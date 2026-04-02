#!/bin/bash

# 简化版部署Ghost到fnos服务器

echo "开始部署Ghost到fnos..."

# 定义变量
LOCAL_DIR="/Users/pangxingzhong/.openclaw/workspace/Ghost"
REMOTE_DIR="~/ghost"

# 1. 连接到fnos服务器并创建部署目录
echo "连接到fnos服务器..."
ssh fnos "mkdir -p $REMOTE_DIR"

# 2. 传输必要的文件到fnos服务器
echo "传输文件到fnos服务器..."
scp -r "$LOCAL_DIR/ghost" fnos:"$REMOTE_DIR/"

# 3. 在fnos上创建虚拟环境并安装主要依赖
echo "在fnos上创建虚拟环境并安装依赖..."
ssh fnos "cd $REMOTE_DIR && python3 -m venv venv && source venv/bin/activate && pip install pycryptodome pyyaml rsa netaddr ecdsa==0.13 paramiko==2.0.2 urllib3==1.26.20 psutil netifaces pylzma colorama mss==4.0.3 pyOpenSSL scapy impacket dnslib cerberus logutils secretstorage==2.3.1 ed25519==1.5 pygments requests tornado win_inet_pton scandir msgpack==0.6.2 hexdump M2Crypto>=0.30.1 fusepy defusedxml keyboard==0.13.4 dateparser puttykeys pyelftools filemagic xattr dukpy pyaes chardet tqdm"

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