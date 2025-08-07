# redroid-frida-hook

基于 redroid 的 frida hook 项目，使用 Frida 在 Android 容器中实现 RPC 调用，用于生成淘宝 API 请求所需的签名。

## 项目介绍

本项目利用 [redroid](https://github.com/remote-android/redroid-doc) (Remote-Android) 技术创建一个 Android 11 容器环境，在其中以运行淘宝应用为例并通过 Frida Hook 技术主动调用，实现远程调用生成淘宝 x-sign 等请求头参数。该方案可以用于获取淘宝订单等数据。

## 工作原理

1. 使用 redroid 创建 Android 11 容器环境
2. 在容器中预装淘宝应用 taobao_monitor.sh 用于保证应用闪退时自动重启
3. 通过 Frida Server Hook 淘宝应用中的签名算法
4. 使用 Python 编写的客户端通过 RPC 调用获取加密参数
5. 使用加密参数向淘宝服务器发起合法请求

## 环境要求

- Linux 系统 (推荐 Ubuntu 20.04+)
- Docker 和 Docker Compose
- Python 3.8+
- ADB 工具
- frida-16.6.6

## 安装 Docker

./install_docker.sh

## 解压 frida

xz -d files/frida-server-x86_64.xz

## 启动 redroid 容器

./run_redroid.sh

## 运行主程序

python main.py

## 作者联系方式

- wx: __int64
- qq: 1415662711