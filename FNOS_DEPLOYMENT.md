# Ghost C2 FNOS 部署指南

## 快速部署

### 方式一：直接在 FNOS 上构建（推荐，首次）

```bash
# 修改脚本中的 FNOS IP
nano deploy/deploy_to_fnos_v2.sh

# 执行部署
bash deploy/deploy_to_fnos_v2.sh [FNOS_IP] [SSH_PORT] build

# 示例
bash deploy/deploy_to_fnos_v2.sh 192.168.1.100 22 build
```

### 方式二：本地构建后导入镜像（网络慢时使用）

```bash
# 1. 本地构建镜像
docker build -t ghost-c2:fnos -f Dockerfile .
docker build -t ghost-websocket:fnos -f Dockerfile.websocket .

# 2. 导出镜像
docker save ghost-c2:fnos ghost-websocket:fnos -o ghost-images.tar

# 3. 部署（使用 import 模式）
bash deploy/deploy_to_fnos_v2.sh [FNOS_IP] [SSH_PORT] import
```

## 部署后访问

- **WebUI**: `http://<fnos-ip>:8089`
- **Ghost C2 HTTPS**: `https://<fnos-ip>:443`
- **Ghost C2 HTTP**: `http://<fnos-ip>:80`
- **WebSocket**: `ws://<fnos-ip>:8766`

## 服务管理

```bash
# 查看日志
ssh root@fnos 'cd /opt/ghost-c2 && docker-compose -f docker-compose.fnos.yml logs -f'

# 重启服务
ssh root@fnos 'cd /opt/ghost-c2 && docker-compose -f docker-compose.fnos.yml restart'

# 停止服务
ssh root@fnos 'cd /opt/ghost-c2 && docker-compose -f docker-compose.fnos.yml down'

# 查看状态
ssh root@fnos 'cd /opt/ghost-c2 && docker-compose -f docker-compose.fnos.yml ps'
```

## 凭据

首次启动后，凭据会自动生成在：
- FNOS 容器内: `/opt/ghost-c2/ghost/.ghost/crypto/credentials.py`
- 持久化卷: `docker volume inspect ghost-ghost-config`

**重要**: 检查生成的凭据是否为随机值（不应有默认密码）。

## 故障排除

### 1. Docker 未运行
```bash
ssh root@fnos 'dockerd &'
# 或
ssh root@fnos '/etc/init.d/docker start'
```

### 2. 端口冲突
检查 FNOS 防火墙：
```bash
ssh root@fnos 'iptables -L -n'
# 开放端口
ssh root@fnos 'iptables -A INPUT -p tcp --dport 8089 -j ACCEPT'
ssh root@fnos 'iptables -A INPUT -p tcp --dport 443 -j ACCEPT'
ssh root@fnos 'iptables -A INPUT -p tcp --dport 8766 -j ACCEPT'
```

### 3. 容器启动失败
查看日志：
```bash
ssh root@fnos 'cd /opt/ghost-c2 && docker-compose -f docker-compose.fnos.yml logs'
```

### 4. WebUI 无法连接 WebSocket
检查 WebSocket 容器状态：
```bash
ssh root@fnos 'docker ps | grep ghost-websocket'
ssh root@fnos 'docker logs ghost-websocket'
```

## 文件清单

```
deploy/
├── deploy_to_fnos_v2.sh      # 主部署脚本（可执行）
├── docker/
│   ├── Dockerfile            # 旧版 FNOS Dockerfile（备用）
│   └── docker-compose.yml    # 旧版配置（备用）
└── README_FNOS.md            # 本文档

项目根目录：
├── docker-compose.fnos.yml   # FNOS 专用编排
├── Dockerfile                # Ghost C2 镜像
├── Dockerfile.websocket      # WebSocket 镜像
├── requirements.txt          # Python 依赖
└── ghost/
    ├── cli/                  # CLI 入口
    ├── ghostlib/             # 核心库
    └── webui/                # React WebUI
        ├── dist/             # 构建产物
        └── nginx.conf        # nginx 配置
```

## 安全建议

1. **修改默认管理员密码**（WebUI）
2. **上传自定义 SSL 证书** 替换自签名证书
3. **配置 FNOS 防火墙** 仅允许信任的 IP 访问
4. **定期备份** `/opt/ghost-c2/data` 卷
5. **启用 HTTPS 重定向**（nginx 配置）

## 更新升级

```bash
# 拉取最新代码
git pull

# 重新部署
bash deploy/deploy_to_fnos_v2.sh [FNOS_IP] build

# 或使用 import 模式（如果本地已构建）
bash deploy/deploy_to_fnos_v2.sh [FNOS_IP] import
```

## 性能优化

FNOS 默认资源限制较严，如需提升性能：

1. 编辑 `/etc/docker/daemon.json`：
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

2. 重启 Docker：
```bash
ssh root@fnos '/etc/init.d/docker restart'
```

3. 调整容器资源（在 docker-compose.fnos.yml 中添加）：
```yaml
services:
  ghost-c2:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

---

**问题反馈**: 请查看 `docker-compose logs` 或提交 Issue
