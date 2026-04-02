#!/bin/bash

# 部署Ghost C2到fnos服务器

echo "开始部署Ghost C2到fnos服务器..."

# 定义变量
LOCAL_DIR="/Users/pangxingzhong/.openclaw/workspace/Ghost"
REMOTE_DIR="~/ghost"

# 1. 连接到fnos服务器并创建部署目录
echo "连接到fnos服务器..."
ssh fnos "mkdir -p $REMOTE_DIR"

# 2. 传输项目文件到fnos服务器
echo "传输项目文件到fnos服务器..."
scp -r "$LOCAL_DIR"/* fnos:"$REMOTE_DIR/"

# 3. 安装系统依赖
echo "安装系统依赖..."
ssh fnos "echo 'Pang1983813AbC' | sudo -S apt-get update && echo 'Pang1983813AbC' | sudo -S apt-get install -y python3 python3-pip python3-venv nginx"

# 4. 配置nginx
echo "配置nginx..."
ssh fnos "echo 'Pang1983813AbC' | sudo -S rm -rf /var/www/ghost/*"
ssh fnos "echo 'Pang1983813AbC' | sudo -S mkdir -p /var/www/ghost"
ssh fnos "echo 'Pang1983813AbC' | sudo -S cp -r $REMOTE_DIR/ghost/webui/dist/* /var/www/ghost/"
# 创建nginx配置文件
ssh fnos 'echo "Pang1983813AbC" | sudo -S sh -c "echo \"server {\n    listen 8089;\n    server_name ghost.zhuquejiasu.uk;\n\n    location / {\n        root /var/www/ghost;\n        index index.html;\n        try_files \$uri \$uri/ /index.html;\n    }\n\n    # 处理WebSocket连接\n    location /ws {\n        proxy_pass http://localhost:8766;\n        proxy_http_version 1.1;\n        proxy_set_header Upgrade \$http_upgrade;\n        proxy_set_header Connection upgrade;\n        proxy_set_header Host \$host;\n    }\n}\" > /etc/nginx/sites-available/ghost"'
ssh fnos "echo 'Pang1983813AbC' | sudo -S ln -sf /etc/nginx/sites-available/ghost /etc/nginx/sites-enabled/"
ssh fnos "echo 'Pang1983813AbC' | sudo -S nginx -t"
ssh fnos "echo 'Pang1983813AbC' | sudo -S systemctl restart nginx"

# 5. 安装WebSocket服务依赖
echo "安装WebSocket服务依赖..."
ssh fnos "cd $REMOTE_DIR && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip setuptools wheel && pip install websockets"

# 6. 启动Ghost C2服务
echo "启动Ghost C2服务..."
# 停止旧的进程
ssh fnos "pkill -f 'python server.py' || true"

# 启动WebSocket服务
ssh fnos "cd $REMOTE_DIR/ghost/webui && source $REMOTE_DIR/venv/bin/activate && nohup python server.py > $REMOTE_DIR/websocket.log 2>&1 &"

# 等待WebSocket服务启动
echo "等待WebSocket服务启动..."
ssh fnos "sleep 5"

# 7. 验证部署
echo "验证部署..."
# 检查WebSocket服务是否正在运行
ssh fnos "ps aux | grep 'python server.py' | grep -v grep"
# 检查WebUI是否可以访问
ssh fnos "curl -I http://localhost:80"
# 检查nginx服务是否正在运行
ssh fnos "echo 'Pang1983813AbC' | sudo -S systemctl status nginx | grep Active"

# 8. 检查日志
echo "检查Ghost服务日志..."
ssh fnos "tail -n 20 $REMOTE_DIR/websocket.log"

echo "部署完成！"
echo "您可以通过以下地址访问Ghost C2："
echo "- Ghost WebUI: http://192.168.1.98:80"
echo "- WebSocket服务: ws://192.168.1.98:8766"