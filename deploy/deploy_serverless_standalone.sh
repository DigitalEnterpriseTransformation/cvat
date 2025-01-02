#!/bin/bash

NUCTL_VERSION=1.13.0

# 安装nuctl命令行工具
if ! command -v nuctl &> /dev/null
then
    echo "正在安装nuctl..."
    wget https://github.com/nuclio/nuclio/releases/download/$NUCTL_VERSION/nuctl-$NUCTL_VERSION-linux-amd64
    sudo mv nuctl-$NUCTL_VERSION-linux-amd64 /usr/local/bin/nuctl && chmod +x /usr/local/bin/nuctl
fi

# 部署nuclio dashboard
echo "正在部署nuclio dashboard..."
docker compose -f docker-compose.serverless.standalone.yml up -d

echo "Done!"
