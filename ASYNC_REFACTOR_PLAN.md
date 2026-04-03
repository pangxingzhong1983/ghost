# Ghost C2 异步化架构重构方案

## 1. 当前架构分析

### 1.1 核心组件

**GhostServer** (`ghost/ghostlib/GhostServer.py`)
- 基于 `threading.Thread` 的并发模型
- 每个客户端连接使用独立的 `GhostConnectionThread`
- 主循环阻塞在 `serve_forever()`

**关键类**:
- `Listener` (Thread) - 监听线程，接受连接
- `GhostConnectionThread` (Thread) - 处理单个客户端连接
- `GhostJob` - 作业管理
- `GhostWeb` - 基于 Tornado 的 Web UI（已部分异步）

### 1.2 同步阻塞点

```python
# GhostConnectionThread.run() 主要循环
while not self._stop.is_set():
    try:
        self._poll_transport()  # 阻塞读取
        self.handle_client()
    except EOFError:
        break
```

**阻塞操作**:
- `socket.recv()` / `send()` - 网络 I/O
- `subprocess.Popen().communicate()` - 进程执行
- `importlib.import_module()` - 模块加载（磁盘 I/O）
- 文件操作（上传/下载）

### 1.3 现有异步基础

**Tornado** 已作为依赖，用于 Web UI - 可重用其 IOLoop

---

## 2. 重构目标

1. **提升并发能力** - 支持数千并发连接（当前受限于线程）
2. **降低内存开销** - 线程栈 ~8MB，协程 ~KB
3. **改善响应性** - 避免单个慢操作阻塞所有连接
4. **保持兼容性** - 模块系统、RPC 接口基本不变

---

## 3. 技术选型

### 3.1 asyncio + aiohttp（推荐）

**优势**:
- Python 标准库，无需额外依赖
- 生态成熟，aiohttp 提供完整 HTTP 服务器/客户端
- 与 Tornado 可互操作（asyncio 托管的 Tornado）

**挑战**:
- 需要重写所有阻塞操作为 async/await
- 同步模块可能无法直接使用（需 thread pool）
- RPC 库（rpyc）需适配异步

### 3.2 混合模式（渐进式迁移）

保留现有线程模型，仅将 I/O 操作异步化：
- 主服务器保持同步
- 使用 `concurrent.futures.ThreadPoolExecutor` 执行阻塞模块
- 使用 `asyncio` 管理网络 I/O

**优势**: 风险低，可增量迁移
**劣势**: 收益有限，仍受限于线程数

### 3.3 Trio（实验性）

更现代的协程库，但增加新依赖

---

## 4. 重构路线图 (6 个月)

### Phase 1: 基础设施 (1-2 周)

- [ ] 引入 `asyncio` 依赖
- [ ] 创建 `ghost/async/` 包
- [ ] 编写异步网络基类 `AsyncGhostSocketServer`
- [ ] 单元测试：验证 asyncio 事件循环

### Phase 2: 核心 I/O 异步化 (3-4 周)

#### 2.1 网络层
- [ ] 重写 `GhostTCPServer` 为 `AsyncGhostTCPServer`
- [ ] 实现 `AsyncGhostConnection`
- [ ] 迁移 `Listener` 使用 `asyncio.start_server()`
- [ ] 保持 `GhostConnectionThread` 接口兼容

#### 2.2 传输协议
- [ ] 所有 `transport` 改为 async
- [ ] `chain_transports` 使用 async 上下文管理器
- [ ] SSL/TLS 包装器 -> `ssl.SSLSocket` 的异步包装

#### 2.3 作业管理
- [ ] `GhostJob` 改为 `asyncio.Task`
- [ ] 超时、取消使用 asyncio 机制

### Phase 3: 阻塞操作迁移 (4-6 周)

#### 3.1 模块执行
```python
# Old
module.run(args)

# New
loop = asyncio.get_running_loop()
await loop.run_in_executor(None, module.run, args)
```

#### 3.2 文件 I/O
- [ ] `aiofiles` 用于异步文件操作
- [ ] 上传/下载使用流式处理

### Phase 4: 测试与验证 (2-3 周)

- [ ] 单元测试覆盖率 > 80%
- [ ] 压力测试：1000+ 并发连接
- [ ] 回归测试：确保现有模块仍工作

### Phase 5: 部署与迁移 (1-2 周)

- [ ] 双模式支持（同步/异步），通过配置切换
- [ ] 迁移文档
- [ ] 监控报警（连接数、延迟）

---

## 5. 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 破坏现有模块兼容性 | 高 | 高 | 保持同步 API，使用适配器模式 |
| 性能提升不达预期 | 中 | 中 | 分阶段性能测试，及时调整 |
| asyncio 学习曲线 | 中 | 低 | 团队培训，代码审查 |
| 第三方库不兼容 | 中 | 中 | 使用线程池隔离阻塞调用 |

---

## 6. 具体代码示例

### 6.1 异步 Listener

```python
# 当前
class Listener(Thread):
    def run(self):
        self.server = GhostTCPServer(...)
        self.server.serve_forever()

# 目标
class AsyncListener:
    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.address, self.port
        )
        await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        conn = AsyncGhostConnection(reader, writer)
        asyncio.create_task(conn.process())
```

### 6.2 异步作业队列

```python
class AsyncGhostJobQueue:
    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._workers: list[asyncio.Task] = []

    async def submit(self, job):
        await self._queue.put(job)

    async def worker(self):
        while True:
            job = await self._queue.get()
            try:
                await job.run()  # async
            except Exception as e:
                logger.error(f"Job failed: {e}")
```

### 6.3 线程池适配器

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=50)

async def run_module_sync(module, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, module.run, *args)
```

---

## 7. 性能预期

| 指标 | 当前 (threading) | 目标 (asyncio) | 提升 |
|------|------------------|----------------|------|
| 并发连接数 | ~200 | 1000+ | 5x |
| 内存/连接 | ~8MB (stack) | ~2KB | 4000x |
| CPU 利用率 | 低 (GIL) | 中高 | 2-3x |
| 响应时间 p99 | 高 | 低 | 50% |

---

## 8. 结论与建议

**推荐采用渐进式异步重构**:

1. **短期**: 在 GhostWeb 和文件传输模块asyncio
2. **中期**: 重构 `GhostTCPServer` 和 `Listener`
3. **长期**: 全栈异步，考虑移除 `threading`

**不建议一次性重写**，风险高、周期长。

**立即可执行的改进**:
- 使用 `asyncio` 的 `ThreadPoolExecutor` 提升并发
- 将 `socket` 操作改为非阻塞 + `selectors`
- 优化 `GhostJob` 队列，减少锁竞争

---

**评估团队**: 需要至少 1 名熟悉 asyncio 的工程师
**预计工时**: 4-6 人月（全量重构）
**优先级**: P3（不影响当前使用，但长期收益大）
