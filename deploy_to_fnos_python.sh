#!/bin/bash

# 部署Python版本的Ghost到fnos服务器

echo "开始部署Python版本的Ghost到fnos..."

# 定义变量
LOCAL_DIR="/Users/pangxingzhong/.openclaw/workspace/Ghost"
REMOTE_DIR="~/ghost"

# 1. 连接到fnos服务器并创建部署目录
echo "连接到fnos服务器..."
ssh fnos "mkdir -p $REMOTE_DIR"

# 2. 传输必要的文件到fnos服务器
echo "传输文件到fnos服务器..."
scp -r "$LOCAL_DIR/ghost" "$LOCAL_DIR/requirements.txt" fnos:"$REMOTE_DIR/"

# 3. 在fnos上创建虚拟环境并安装依赖
echo "在fnos上创建虚拟环境并安装依赖..."
ssh fnos "cd $REMOTE_DIR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"

# 4. 启动Ghost服务
echo "启动Ghost服务..."
ssh fnos "cd $REMOTE_DIR && source venv/bin/activate && nohup python -m ghost.cli > ghost.log 2>&1 &"

# 5. 验证部署
echo "验证部署..."
ssh fnos "ps aux | grep ghost"

# 6. 检查日志
echo "检查Ghost服务日志..."
ssh fnos "tail -n 20 $REMOTE_DIR/ghost.log"

echo "部署完成！"
echo "Ghost服务已在fnos服务器上启动。"