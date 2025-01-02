#!/bin/bash

# 需要提供本机ip才可以从外部访问
if [ -z $CVAT_HOST ]
then
    echo "请在配置CVAT_HOST环境变量之后再运行此脚本"
fi

NUCTL_VERSION=1.13.0

# 安装nuctl命令行工具
if ! command -v nuctl &> /dev/null
then
    echo "正在安装nuctl..."
    wget https://github.com/nuclio/nuclio/releases/download/$NUCTL_VERSION/nuctl-$NUCTL_VERSION-linux-amd64
    sudo mv nuctl-$NUCTL_VERSION-linux-amd64 /usr/local/bin/nuctl && chmod +x /usr/local/bin/nuctl
fi

echo "正在部署CVAT及nuclio dashboard..."
docker compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml up -d

echo "Done!"
