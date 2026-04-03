#!/bin/bash
#
# Ghost C2 简单部署脚本 - 不使用外部 Docker 镜像
# 利用 FNOS 现有 Python 环境
#
set -e

FNOS_HOST="fnos"
SSH_PORT=22
REMOTE_DIR="/opt/ghost-c2"

echo "=== Ghost C2 FNOS 简单部署 ==="

# SSH 连接测试
echo -n "测试 SSH 连接..."
if ssh -p "$SSH_PORT" "$FNOS_HOST" "echo ok" 2>/dev/null | grep -q ok; then
    echo "成功"
else
    echo "失败"
    exit 1
fi

# 准备文件
echo "准备文件..."
tar --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' --exclude='build' \
    --exclude='dist' --exclude='*.egg-info' --exclude='node_modules' \
    -czf /tmp/ghost-simple-deploy.tar.gz -C .. ghost/ requirements.txt

# 上传
echo "上传到 FNOS..."
ssh "$FNOS_HOST" "sudo -S <<< 'Pang1983813AbC' mkdir -p $REMOTE_DIR"
scp /tmp/ghost-simple-deploy.tar.gz "$FNOS_HOST:/tmp/"

# 远程执行
ssh "$FNOS_HOST" bash -c "'
set -e
cd $REMOTE_DIR
echo \"Pang1983813AbC\" | sudo -S cp /tmp/ghost-simple-deploy.tar.gz .
tar -xzf ghost-simple-deploy.tar.gz && rm ghost-simple-deploy.tar.gz

# 检查 Python
if ! command -v python3 &>/dev/null; then
    echo \"Python3 未安装\"
    exit 1
fi

# 安装依赖
echo \"安装 Python 依赖...\"
sudo -S <<< \"Pang1983813AbC\" pip3 install --no-cache-dir -r requirements.txt

# 测试运行
echo \"测试 Ghost CLI...\"
cd ghost
sudo -S <<< \"Pang1983813AbC\" python3 ghost/cli/ghostsh.py --help

echo \"部署完成\"
'"

echo "✓ 部署成功"
