# 部署方法
## 只部署CVAT
serverless模型服务用于自动标注，如果不需要自动标注，可以只部署CVAT。

1. 设置环境变量CVAT_HOST为服务器IP

2. 在cvat根目录下运行
```bash
bash deploy/deploy_cvat_standalone.sh
```

## CVAT和serverless模型服务部署在同一台服务器
1. 设置环境变量CVAT_HOST为服务器IP

2. 在cvat根目录下运行
```bash
bash deploy/deploy_cvat_and_local_serverless.sh
```

## CVAT和serverless模型服务部署在不同的服务器
1. 在需要部署serverless模型服务的机器上运行
```bash
bash deploy/deploy_serverless_standalone.sh
```

2. 在需要部署cvat的机器上配置环境变量
    - 设置CVAT_HOST为服务器IP
    - 设置CVAT_NUCLIO_HOST为serverless服务器IP

3. 在需要部署cvat的机器上运行
```bash
# 有两种调用serverless服务的方式：dashboard和direct，默认为direct
# 目前不清楚两种方式会有什么区别

# direct模式
bash deploy/deploy_cvat_with_remote_serverless.sh
# 或者
bash deploy/deploy_cvat_with_remote_serverless.sh direct

# dashboard模式
bash deploy/deploy_cvat_with_remote_serverless.sh dashboard
```

## 部署自动标注模型
TODO