#!/bin/bash
#
# Ghost C2 全自动 FNOS 部署脚本
# 零人工干预，自动检测、配置、启动
#

set -e

# 配置（请根据实际情况修改）
FNOS_IP="192.168.1.198"
SSH_USER="root"
SSH_PASS="Pang1983813AbC"
SSH_PORT=22
REMOTE_DIR="/opt/ghost-c2"

# 颜色
G='\033[0;32m'; R='\033[0;31m'; Y='\033[1;33m'; N='\033[0m'

echo -e "${G}[*] Ghost C2 全自动 FNOS 部署${N}"

# 1. SSH 自动登录函数
ssh_auto() {
    sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -p "$SSH_PORT" "$SSH_USER@$FNOS_IP" "$@"
}

scp_auto() {
    sshpass -p "$SSH_PASS" scp -P "$SSH_PORT" -o StrictHostKeyChecking=no "$@"
}

# 2. 检测环境
echo -e "${Y}[1] 检测 FNOS 环境...${N}"
if ! ssh_auto "echo" 2>/dev/null; then
    echo -e "${R}[!] SSH 连接失败，请检查 IP/密码${N}"
    exit 1
fi

# 3. 准备部署包
echo -e "${Y}[2] 准备部署包...${N}"
TMP_TAR="/tmp/ghost_fnos_$(date +%s).tar.gz"
tar --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' --exclude='build' \
    --exclude='dist' --exclude='*.egg-info' --exclude='node_modules' \
    -czf "$TMP_TAR" docker-compose.fnos.yml Dockerfile Dockerfile.websocket requirements.txt ghost/ 2>/dev/null || true

# 4. 上传文件
echo -e "${Y}[3] 上传文件到 FNOS...${N}"
ssh_auto "mkdir -p '$REMOTE_DIR' && cd '$REMOTE_DIR' && rm -rf ghost-deploy.tar.gz"
scp_auto "$TMP_TAR" "$SSH_USER@$FNOS_IP:$REMOTE_DIR/ghost-deploy.tar.gz"
rm -f "$TMP_TAR"

# 5. 远程执行部署
echo -e "${Y}[4] 在 FNOS 上执行部署...${N}"
ssh_auto "bash -c \"set -e
cd '$REMOTE_DIR'

# 解压
echo '解压...'
tar -xzf ghost-deploy.tar.gz && rm ghost-deploy.tar.gz

# 检测 Docker
if ! command -v docker &>/dev/null; then
    echo 'Docker 未安装，安装中...'
    opkg update
    opkg install docker
    rc-update add docker default
    /etc/init.d/docker start
    sleep 3
fi

# 检测 Docker Compose
if ! docker compose version &>/dev/null; then
    echo '安装 Docker Compose...'
    apk add --no-cache py3-pip
    pip3 install docker-compose
fi

# 创建数据目录
mkdir -p data

# 构建或运行
echo '构建镜像...'
docker compose -f docker-compose.fnos.yml build --no-cache

# 启动
echo '启动服务...'
docker compose -f docker-compose.fnos.yml down 2>/dev/null || true
docker compose -f docker-compose.fnos.yml up -d

# 等待
sleep 5
docker compose -f docker-compose.fnos.yml ps
echo '部署完成'
\""

# 6. 验证服务
echo -e "${Y}[5] 验证服务...${N}"
sleep 3
ssh_auto "cd '$REMOTE_DIR' && docker compose -f docker-compose.fnos.yml ps" 2>/dev/null || true

# 7. 输出访问信息
echo
echo -e "${G}[✓] 部署完成！${N}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "访问地址:"
echo "  WebUI:    http://$FNOS_IP:8089"
echo "  C2 HTTPS: https://$FNOS_IP:443"
echo "  C2 HTTP:  http://$FNOS_IP:80"
echo "  WebSocket: ws://$FNOS_IP:8766"
echo
echo "管理命令:"
echo "  ssh $SSH_USER@$FNOS_IP 'cd $REMOTE_DIR && docker compose -f docker-compose.fnos.yml logs -f'"
echo "  ssh $SSH_USER@$FNOS_IP 'cd $REMOTE_DIR && docker compose -f docker-compose.fnos.yml restart'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
