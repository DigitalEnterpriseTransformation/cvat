#!/bin/bash

# 需要提供本机ip才可以从外部访问
if [ -z $CVAT_HOST ]
then
    echo "请在配置CVAT_HOST环境变量之后再运行此脚本"
fi

# 需要提供远程nuclio host ip
if [ -z $CVAT_NUCLIO_HOST ]
then
    echo "请在配置CVAT_NUCLIO_HOST环境变量之后再运行此脚本"
fi

if [ -z $1 ]
then
    # nuclio调用方式默认direct
    nuclio_invoke_method="direct"
else
    nuclio_invoke_method=$1
fi

echo "nuclio调用方式$nuclio_invoke_method"

# 根据调用方式选择docker compose override文件
if [ $nuclio_invoke_method == "direct" ]
then
    docker_compose_override_file=components/serverless/docker-compose.serverless.override.direct.yml
elif [ $nuclio_invoke_method == "dashboard" ]
then
    docker_compose_override_file=components/serverless/docker-compose.serverless.override.dashboard.yml
else
    echo "请输入正确的nuclio调用方式，dashboard或者direct"
fi

echo "正在部署CVAT..."
docker compose -f docker-compose.yml -f $docker_compose_override_file up -d

echo "Done!"
