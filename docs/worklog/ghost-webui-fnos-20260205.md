# 工作说明文档：Ghost Web UI（fnos + Docker + CF Tunnel）

## 1. 用户需求、任务目的与背景
目标是在 fnos 的 Docker 中部署 Ghost Web UI，提供配置管理、日志、任务编排、历史记录、审计与多用户登录，并通过 Cloudflare Tunnel 暴露域名 `ghost.zhuquejiasu.uk`，端口使用 `8089`。初始管理员账号为 `pangxingzhong@gmail.com`，允许后台新增用户，且允许执行 `!` 开头的系统命令。

## 2. 本次所有变更点（逐条罗列）
1. 新增 Web UI 后端（Tornado）：认证、任务队列、配置管理、用户管理、审计、日志接口。
2. 新增 Web Terminal（WebSocket + PTY），提供完整 CLI 控制台能力。
3. 新增 Web UI 前端静态页面（Dashboard/Tasks/Terminal/Config/Users/Audit/Logs）。
4. 新增 Dockerfile 与 docker-compose（包含 cloudflared）。
5. 新增 systemd 服务文件（Docker Compose 常驻与自启）。
6. 新增工作说明文档。
7. 修复 Web UI 启动时的循环导入：在 `ghost/webui/runtime.py` 预置 `sys.__ghost_main__=True` 并改为直接导入 `GhostConfig/GhostServer/Credentials` 子模块，避免 `ghost.ghostlib` 在初始化时加载 `GhostCmdLoop` 导致 `ghost.commands` 循环引用。
8. 修复 Cloudflare Tunnel 503：新增 `deploy/docker/cloudflared.yml` ingress 映射，并让 compose 挂载该配置供 cloudflared 使用。
9. Web UI 中文化：更新 `ghost/webui/static/index.html` 与 `ghost/webui/static/app.js` 的界面文案与状态显示为中文。

## 3. 变更前后差异对照（diff 摘要）

```diff
ghost/webui/runtime.py
ghost/webui/server.py
ghost/webui/handlers_core.py
ghost/webui/handlers_admin.py
ghost/webui/terminal.py
ghost/webui/static/index.html
ghost/webui/static/app.js
ghost/webui/static/app.css
deploy/docker/Dockerfile
deploy/docker/docker-compose.yml
deploy/docker/cloudflared.yml
deploy/systemd/ghost-webui.service
docs/worklog/ghost-webui-fnos-20260205.md
ghost/webui/auth.py (新增用户管理函数)
ghost/webui/__main__.py
ghost/webui/tasks.py
ghost/webui/__init__.py (已存在，无变更)
ghost/webui/db.py (已存在，无变更)
```

## 4. 最终代码使用方式、依赖条件与注意事项
### 部署目录规划（fnos）
- 数据卷根目录：`/vol2/1000/Docker/ghost`
- 源码目录：`/vol2/1000/Docker/ghost/app`（放置 Ghost 仓库）
- 运行数据目录：`/vol2/1000/Docker/ghost/data`（自动生成）
- Compose 文件：`/vol2/1000/Docker/ghost/docker-compose.yml`

### 启动命令（fnos）
```bash
cd /vol2/1000/Docker/ghost
export TUNNEL_TOKEN="YOUR_CF_TUNNEL_TOKEN"
docker compose up -d --build
```

### Web UI 访问
- 内网访问：`http://<fnos-ip>:8089`
- 外网访问：通过 Cloudflare Tunnel 绑定域名 `ghost.zhuquejiasu.uk`

### Cloudflare Tunnel 配置说明
需要在 Cloudflare Tunnel 里将 `ghost.zhuquejiasu.uk` 指向 `http://ghost-webui:8089`。
同时本项目提供 `deploy/docker/cloudflared.yml`，容器会使用该 ingress 映射（无映射会导致 503）。

### systemd 开机自启
```bash
sudo cp /vol2/1000/Docker/ghost/app/deploy/systemd/ghost-webui.service /etc/systemd/system/ghost-webui.service
sudo systemctl daemon-reload
sudo systemctl enable ghost-webui.service
sudo systemctl start ghost-webui.service
```

### 验证步骤
```bash
docker ps --filter "name=ghost-webui"
curl -s http://127.0.0.1:8089/api/health
systemctl status ghost-webui.service --no-pager
systemctl list-timers --all | grep ghost-webui || true
journalctl -u ghost-webui.service -n 200 --no-pager
```
补充执行结果（2026-02-06）：已在 fnos 重新构建 `ghost-ghost-webui` 镜像并重启 `ghost-webui`，`curl http://127.0.0.1:8089/api/health` 返回 `{"ok": true, ...}`。
补充执行结果（2026-02-06）：cloudflared 已加载 ingress 配置，`curl -I https://ghost.zhuquejiasu.uk` 返回 200。
补充执行结果（2026-02-15）：修复“重启后不自启”问题：将 compose 的重启策略从 `unless-stopped` 调整为 `always`，并在 fnos 安装启用 `ghost-webui.service`（oneshot），开机自动执行 `docker compose up -d`；已验证 `http://127.0.0.1:8089/api/health` 与 `https://ghost.zhuquejiasu.uk/api/health` 均返回 200。
补充执行结果（2026-03-08）：修复手机端登录页适配异常。根因是 `app.css` 中使用 `.login-row`（与 `.row` 选择器同优先级）导致 `display:grid` 被后续 `.row{display:flex}` 覆盖，表现为输入框被压缩、登录按钮横向溢出。修复方式：改为 `.row.login-row`（提高优先级）并同步媒体查询；同时将 `index.html` 的样式版本号从 `v=20260306c` 提升到 `v=20260308a` 以强制刷新缓存。线上已验证移动端恢复为单列输入+按钮布局。

### 注意事项
1. Web Terminal 启动的 `ghostsh` 使用 `--not-encrypt`（避免交互密码阻塞），如需启用加密，可设置 `GHOST_UI_GHOSTSH_ENCRYPT=1`。
2. 任务队列串行执行，命令输出保存在 SQLite 中（`/data/ghostui.db`）。
3. 配置管理写入 `~/.ghost/ghost.conf`（容器内 `HOME=/data`，即 `/data/.ghost/ghost.conf`）。

## 5. 风险点与回滚方案
### 风险点
1. Docker 构建依赖较多，首次构建耗时较长。
2. `ghostsh` 默认禁用加密，会以明文方式生成凭据文件。
3. `!` 命令允许执行系统命令，需确保只给管理员使用。
4. 如出现 `ImportError: cannot import name 'Commands' from partially initialized module 'ghost.commands'`，需要重新构建镜像以生效 `runtime.py` 的循环导入修复。

### 回滚方案
1. 停止并删除容器：`docker compose down`
2. 回滚代码：切换回旧版本目录或恢复 Git 提交。
3. 删除数据卷（谨慎）：删除 `/vol2/1000/Docker/ghost/data` 目录即可回滚配置与数据库。

## 6. 后续可扩展与优化建议
1. 增加任务并行度与任务依赖编排。
2. 引入 RBAC 与更细粒度命令授权策略。
3. Web Terminal 进一步支持按键级输入与快捷键映射。
4. 将审计日志持久化到外部系统（如 ELK 或 Loki）。

## 7. 记忆与可复用信息
已新增 Web UI + Docker + systemd 的完整链路文件，后续可按此结构复用到其他节点。
