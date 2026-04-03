#!/bin/bash
#
# Ghost C2 到 FNOS 的一键部署脚本
# 支持：直接构建或镜像导入
#

set -e

# 配置
FNOS_HOST="root@fnos"  # 修改为实际IP
SSH_PORT=22
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_DIR="/opt/ghost-c2"
COMPOSE_FILE="docker-compose.fnos.yml"

echo "=== Ghost C2 FNOS 部署 ==="
echo "本地目录: $LOCAL_DIR"
echo "远程主机: $FNOS_HOST"
echo

# 检查参数
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "用法: $0 [fnos_host] [ssh_port] [mode]"
    echo "  mode: build (默认) - 在 FNOS 上构建镜像"
    echo "        import - 从本地导入预构建镜像 (需先运行 --export)"
    echo " 示例: $0 192.168.1.1 22 build"
    echo "      : $0 192.168.1.1 22 import"
    exit 0
fi

if [ $# -ge 1 ]; then
    FNOS_HOST="root@$1"
fi
if [ $# -ge 2 ]; then
    SSH_PORT="$2"
fi
MODE="${3:-build}"

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# SSH 连接测试
echo -n "测试 SSH 连接..."
if ssh -p "$SSH_PORT" -o ConnectTimeout=5 "$FNOS_HOST" "echo ok" 2>/dev/null | grep -q ok; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ 连接失败${NC}"
    exit 1
fi

# 准备本地文件
echo "准备部署文件..."
tar -czf /tmp/ghost-deploy.tar.gz -C "$LOCAL_DIR" \
    docker-compose.fnos.yml \
    Dockerfile \
    Dockerfile.websocket \
    requirements.txt \
    ghost/ 2>/dev/null

if [ "$MODE" = "import" ]; then
    # 导出镜像并传输
    echo "导出镜像..."
    docker build -t ghost-c2:fnos -f Dockerfile . 2>/dev/null || true
    docker build -t ghost-websocket:fnos -f Dockerfile.websocket . 2>/dev/null || true
    docker save ghost-c2:fnos ghost-websocket:fnos -o /tmp/ghost-images.tar
    echo "传输镜像和代码..."
    scp -P "$SSH_PORT" /tmp/ghost-images.tar "$FNOS_HOST:$REMOTE_DIR/"
    scp -P "$SSH_PORT" /tmp/ghost-deploy.tar.gz "$FNOS_HOST:$REMOTE_DIR/"
else
    echo "传输代码（将在 FNOS 上构建）..."
    scp -P "$SSH_PORT" /tmp/ghost-deploy.tar.gz "$FNOS_HOST:$REMOTE_DIR/"
fi

# 远程执行部署
ssh -t -p "$SSH_PORT" "$FNOS_HOST" bash -c "'
set -e
cd $REMOTE_DIR || exit 1

echo '=== FNOS 部署脚本 ==='

# 解压
if [ ! -f ghost-deploy.tar.gz ]; then
    echo '错误: 未找到 ghost-deploy.tar.gz'
    exit 1
fi
tar -xzf ghost-deploy.tar.gz && rm ghost-deploy.tar.gz

# Docker 环境检查
if ! command -v docker &>/dev/null; then
    echo 'Docker 未安装，尝试安装...'
    opkg update
    opkg install docker
    rc-update add docker default
    /etc/init.d/docker start
    sleep 3
fi

# 构建或加载镜像
if [ '$MODE' = 'import' ] && [ -f ghost-images.tar ]; then
    echo '加载镜像...'
    docker load < ghost-images.tar
    rm ghost-images.tar
else
    echo '构建 Docker 镜像...'
    docker-compose -f $COMPOSE_FILE build --no-cache
fi

# 创建数据目录
mkdir -p data

# 启动服务
echo '启动服务...'
docker-compose -f $COMPOSE_FILE down 2>/dev/null || true
docker-compose -f $COMPOSE_FILE up -d

# 等待启动
sleep 5
docker-compose -f $COMPOSE_FILE ps

echo '=== 部署完成 ==='
'"

# 获取 IP
IP=$(echo "$FNOS_HOST" | sed 's/.*@//')
echo
echo -e "${GREEN}部署成功!${NC}"
echo "访问地址:"
echo "  WebUI:   http://$IP:8089"
echo "  C2:      https://$IP:443"
echo "  WS:      ws://$IP:8766"
echo
echo "查看日志: ssh -p $SSH_PORT $FNOS_HOST 'cd $REMOTE_DIR && docker-compose -f $COMPOSE_FILE logs -f'"
