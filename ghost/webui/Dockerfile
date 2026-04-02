# 使用nginx作为基础镜像
FROM nginx:alpine

# 复制构建后的静态文件到nginx的html目录
COPY dist/ /usr/share/nginx/html/

# 复制自定义的nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]