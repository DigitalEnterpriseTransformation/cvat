#!/bin/bash

# 需要提供本机ip才可以从外部访问
if [ -z $CVAT_HOST ]
then
    echo "请在配置CVAT_HOST环境变量之后再运行此脚本"
fi

echo "正在部署CVAT..."
docker compose -f docker-compose.yml up -d

echo "Done!"
