#!/bin/bash
#
# Ghost C2 FNOS 部署脚本
# 用法: ./deploy_to_fnos.sh [fnos_host] [ssh_port]
#
# 示例: ./deploy_to_fnos.sh 192.168.1.100 22
# 或: ./deploy_to_fnos.sh root@your-fnos-ip
#

set -e

# 配置
FNOS_HOST="${1:-root@fnos}"
SSH_PORT="${2:-22}"
REMOTE_DIR="/opt/ghost-c2"
COMPOSE_FILE="docker-compose.fnos.yml"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Ghost C2 FNOS 部署脚本 ===${NC}"
echo "目标主机: $FNOS_HOST"
echo "SSH 端口: $SSH_PORT"
echo "远程目录: $REMOTE_DIR"
echo

# 检查本地文件是否存在
if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}错误: 找不到 $COMPOSE_FILE${NC}"
    echo "请先在项目根目录生成 FNOS 配置文件"
    exit 1
fi

# 1. 测试 SSH 连接
echo -e "${YELLOW}[1/6] 测试 SSH 连接...${NC}"
if ssh -p "$SSH_PORT" -o ConnectTimeout=10 "$FNOS_HOST" "echo 'SSH 连接成功'"; then
    echo -e "${GREEN}✓ SSH 连接正常${NC}"
else
    echo -e "${RED}✗ 无法连接到 $FNOS_HOST:${SSH_PORT}${NC}"
    exit 1
fi

# 2. 创建远程目录
echo -e "${YELLOW}[2/6] 创建远程目录...${NC}"
ssh -p "$SSH_PORT" "$FNOS_HOST" "mkdir -p '$REMOTE_DIR' && chmod 755 '$REMOTE_DIR'"
echo -e "${GREEN}✓ 远程目录创建完成${NC}"

# 3. 上传 docker-compose.yml
echo -e "${YELLOW}[3/6] 上传部署配置文件...${NC}"
scp -P "$SSH_PORT" "$COMPOSE_FILE" "$FNOS_HOST:$REMOTE_DIR/docker-compose.yml"
scp -P "$SSH_PORT" "Dockerfile" "$FNOS_HOST:$REMOTE_DIR/Dockerfile" 2>/dev/null || echo "警告: 未找到根 Dockerfile，跳过"
scp -P "$SSH_PORT" "requirements.txt" "$FNOS_HOST:$REMOTE_DIR/requirements.txt" 2>/dev/null || echo "警告: 未找到 requirements.txt，跳过"
echo -e "${GREEN}✓ 配置文件上传完成${NC}"

# 4. 上传 WebUI 文件
echo -e "${YELLOW}[4/6] 上传 WebUI 静态文件...${NC}"
# 确保 webui 已构建
if [ ! -d "ghost/webui/dist" ] || [ -z "$(ls -A ghost/webui/dist 2>/dev/null)" ]; then
    echo -e "${YELLOW}WebUI 未构建，正在构建...${NC}"
    (cd ghost/webui && npm install && npm run build)
fi

# 创建远程 webui 目录
ssh -p "$SSH_PORT" "$FNOS_HOST" "mkdir -p '$REMOTE_DIR/ghost/webui/dist'"
# 上传 dist 内容
scp -r -P "$SSH_PORT" ghost/webui/dist/* "$FNOS_HOST:$REMOTE_DIR/ghost/webui/dist/" 2>/dev/null || true
scp -r -P "$SSH_PORT" ghost/webui/nginx.conf "$FNOS_HOST:$REMOTE_DIR/ghost/webui/" 2>/dev/null || true
echo -e "${GREEN}✓ WebUI 文件上传完成${NC}"

# 5. 上传完整 Ghost 源码
echo -e "${YELLOW}[5/6] 上传 Ghost 源码 (可能需要几分钟)...${NC}"
# 排除不需要的文件
TAR_EXCLUDE="--exclude=__pycache__ --exclude=*.pyc --exclude=.git --exclude=build --exclude=dist --exclude=*.egg-info --exclude=.venv --exclude=ghostvenv --exclude=node_modules --exclude=.pytest_cache"
tar -czf /tmp/ghost-c2.tar.gz $TAR_EXCLUDE ghost/ requirements.txt setup.py pyproject.toml README.md 2>/dev/null || true
scp -P "$SSH_PORT" /tmp/ghost-c2.tar.gz "$FNOS_HOST:$REMOTE_DIR/"

# 在远程解压
ssh -p "$SSH_PORT" "$FNOS_HOST" "cd '$REMOTE_DIR' && tar -xzf ghost-c2.tar.gz && rm ghost-c2.tar.gz"
echo -e "${GREEN}✓ Ghost 源码上传完成${NC}"

# 6. 启动服务
echo -e "${YELLOW}[6/6] 启动 Docker 服务...${NC}"
ssh -t -p "$SSH_PORT" "$FNOS_HOST" "cd '$REMOTE_DIR' && \
    echo '正在构建并启动容器...' && \
    docker-compose -f '$COMPOSE_FILE' down 2>/dev/null || true && \
    docker-compose -f '$COMPOSE_FILE' build --no-cache 2>&1 | tail -20 && \
    docker-compose -f '$COMPOSE_FILE' up -d && \
    docker-compose -f '$COMPOSE_FILE' ps"

# 检查服务状态
echo
echo -e "${YELLOW}=== 部署后检查 ==="
sleep 5
ssh -p "$SSH_PORT" "$FNOS_HOST" "cd '$REMOTE_DIR' && docker-compose -f '$COMPOSE_FILE' logs --tail=50" | tail -20

# 获取访问地址
PUBLIC_IP=$(echo "$FNOS_HOST" | sed 's/.*@//')
echo
echo -e "${GREEN}=== 部署完成 ===${NC}"
echo "服务访问地址:"
echo "  WebUI:        http://$PUBLIC_IP:8089"
echo "  Ghost C2:     https://$PUBLIC_IP:443 (自签名证书)"
echo "  WebSocket:    ws://$PUBLIC_IP:8766"
echo
echo "管理命令:"
echo "  查看日志: ssh $FNOS_HOST 'cd $REMOTE_DIR && docker-compose -f $COMPOSE_FILE logs -f'"
echo "  停止服务: ssh $FNOS_HOST 'cd $REMOTE_DIR && docker-compose -f $COMPOSE_FILE down'"
echo "  重启服务: ssh $FNOS_HOST 'cd $REMOTE_DIR && docker-compose -f $COMPOSE_FILE restart'"
echo
echo -e "${YELLOW}请确保 FNOS 防火墙开放以下端口:${NC}"
echo "  8089 (WebUI), 443 (C2 HTTPS), 80 (C2 HTTP), 8766 (WebSocket)"
echo
