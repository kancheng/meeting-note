# Docker

Windows 的版本需要 WSL 跟開啟虛擬化設定。

根據 jupyter

https://hub.docker.com/r/jupyter/datascience-notebook/

執行

```
docker pull jupyter/datascience-notebook
```

完成後即可

FATE 範例 (1.10)

```
docker pull federatedai/standalone_fate:${version}
```

## Docker 外掛目錄

在本地建立一個名為 docker-save 目錄。

```
> docker images

> docker run -it -v D:\docker-save:/share python /bin/bash

> docker run -it -v [本地端目錄]:[Docker 目錄] [Docker 映像的名稱] /bin/bash
```

FATE 範例 1.10

```
docker pull federatedai/standalone_fate:1.10.0
```

可以事先建立好目錄

```
D:\docker\fate-share
```

```
# 掛載目錄寫法
docker run -it -v D:\docker\fate-share:/share dbe096af397a19d210b24230f23e5147298964f99fb05ca25814603e9348840f /bin/bash

# 官方版本
docker run -it --name standalone_fate -p 8080:8080 federatedai/standalone_fate:${version}

# 官方版本 1.10.0
docker run -it --name standalone_fate -p 8080:8080 federatedai/standalone_fate:1.10.0
```

最終版本

```
docker run -it -v D:\docker\fate-share:/share -p 8897:8080 federatedai/standalone_fate:1.10.0 /bin/bash
docker container start standalone_fate
```

## Reference

1. https://github.com/kancheng/FATE/blob/master/deploy/standalone-deploy/README.zh.md

2. https://github.com/FederatedAI/DOC-CHN/blob/master/%E9%83%A8%E7%BD%B2/FATE%E5%8D%95%E6%9C%BA%E9%83%A8%E7%BD%B2%E6%8C%87%E5%8D%97.rst

3. https://www.runoob.com/docker/docker-dockerfile.html

4. https://kanchengzxdfgcv.blogspot.com/search/label/Docker

5. https://www.zhihu.com/question/485726981/answer/2851953497

6. https://blog.csdn.net/Scarlris_Ye/article/details/128585698

# FateBoard

https://github.com/FederatedAI/FATE-Board/blob/master/README-CN.md

從單機的 Docker 可以從其路徑中的檔案找到預設的帳號與密碼。完成後登入。

```
/data/projects/fate/fateboard/conf/application.properties
```

访问容器 FateBoard

http://127.0.0.1:8080，用户名：admin，密码：admin

# WSL 安裝

在 Windows Docker 需要

https://learn.microsoft.com/zh-tw/windows/wsl/install

# WSL Ubuntu & openSUSE

開啟 Windows 虛擬化設定，去 MS 商店進行安裝

openSUSE Leap 15.4 : https://www.microsoft.com/store/productId/9PJPFJHRM62V

Ubuntu 22.04.2 LTS : https://www.microsoft.com/store/productId/9PN20MSR04DW

```
cd /mnt/c/Users/用户名/Downloads/ 
```

# WSA

https://learn.microsoft.com/zh-tw/windows/android/wsa/

Apk Installer For Android Subsystem : https://www.microsoft.com/store/productId/9NVBQJCTJ2WD

## Reference

1. https://zhuanlan.zhihu.com/p/424959704


# Docker 實驗

Test Ubuntu

```
docker run -it -v D:\docker\ubuntu-share:/share [映像名] /bin/bash
```

在單一個目錄下建立起名為 dockerfile 的檔案，內容如下 :

```
# 基礎映像檔
FROM ubuntu:latest

# 維護者
MAINTAINER Kan

# 操作指令
RUN apt-get update -y\
    && apt-get install vim -y

# 設定運行時容器提供服務的通道
EXPOSE 80

```

指令

```
# 將 Dockerfile 用成 image ，ubunvim 是測試名稱
docker build -t ubunvim .

# 檢視 image
docker images

# 執行
docker run -d -p 80:80 --name [容器名] [映像檔名]
docker run -it -v D:\docker\ubuntu-share:/share ubunvim /bin/bash

# 關閉
docker container stop [容器名]

# 開啟
docker container start [容器名]

# 檢視容器
docker ps -a
```

# Docker exec 命令 - 進入與離開

```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

EX :

```
docker exec -it fe8dc /bin/bash
```

-d :分离模式: 在后台运行

-i :即使没有附加也保持STDIN 打开

-t :分配一个伪终端

如果要退出就：Ctrl-D or `exit`

## Reference

1. https://blog.csdn.net/dongdong9223/article/details/52998375


# FATE 容器

一進入容器的路徑主要位置。

```
[root@fe8dc451858b fate]# pwd
/data/projects/fate
[root@fe8dc451858b fate]#
```

先前掛載目錄為 share。所以嘗試輸出 test.py 到 log.txt。

```
print("Hi")
```

```
python /share/test.py > /share/log.txt
```

# WSL Ubuntu & FATE 測試容器

要先安裝 Package

```
sudo apt install net-tools
```

```
sudo netstat -apln|grep 8080
```

# FATE 測試

在容器內的 fate 目錄執行 

```
source bin/init_env.sh
```

```
pip list
```

# 容器外使用 VSCode 访问 fate 服务

官方镜像只开放了fateboard的外部端口8080，如果需要使用外部客户端连接fate server则需要修改容器里 service_conf.yaml，将 9380 端口也开放出去。

步骤如下：

从容器中拷贝一份配置文件 `/data/projects/fate/conf/service_conf.yaml` 到本地 `service_conf.yaml` ，修改 `fateflow` 的 `host` 如下：

```
fateflow:
	host: 0.0.0.0
```

重新启动容器，将本地 `service_conf.yaml` 映射到容器里的 `/data/projects/fate/conf/service_conf.yaml`

在执行 docker run 的时候如果添加 --rm 参数，则容器终止后会立刻删除。--rm参数和-d参数不能同时使用。

```
# Demo :
docker run -it --name fate_local -p 8897:8080 -p 9380:9380 -v d:/[本地路徑]/service_conf.yaml:/data/projects/fate/conf/service_conf.yaml federatedai/standalone_fate:1.10.0

# EX :
docker run -it --name fate_local -p 8897:8080 -p 9380:9380 -v D:/docker/fate-share/service_conf.yaml:/data/projects/fate/conf/service_conf.yaml federatedai/standalone_fate:1.10.0

docker run -rm -it --name fate_local -p 9797:8080 -p 9787:9380 -v D:/docker/fate-share/service_conf.yaml:/data/projects/fate/conf/service_conf.yaml -v D:\docker\fate-share:/share federatedai/standalone_fate:1.10.0

docker run -it --name fate_local -p 9797:8080 -p 9787:9380 -v D:/docker/fate-share/service_conf.yaml:/data/projects/fate/conf/service_conf.yaml -v D:\docker\fate-share:/share federatedai/standalone_fate:1.10.0
```
## 測試 

使用官方的 pipeline_tutorial_upload.ipynb

- https://github.com/FederatedAI/FATE/blob/master/doc/tutorial/pipeline/pipeline_tutorial_upload.ipynb

### 安裝

1. https://pytorch.org/

2. chardet

```
pip install chardet
```

# Docker name & rename


```
docker run --name=container_name
```

使用指令 `docker rename <old_name> <new_name>` 來重新命名 container 名稱。

old_name 是舊的名稱， new_name 為新的名稱。

例如要把名稱將 distracted_stonebraker 改為 jenkins 則輸入

```
docker rename distracted_stonebraker jenkins
```

## Reference

1. https://matthung0807.blogspot.com/2020/10/docker-rename-container-name.html

# Windows Docker 配置中国镜像源

- Docker-Desktop 界面操作和修改 daemon.json 两种方法配置国内镜像源

```
"registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com",
    "http://hub-mirror.c.163.com",
    "https://mirror.ccs.tencentyun.com"
]
```

```
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
```

```
{
  "debug": true,
  "experimental" :true,
  "registry-mirrors" : [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com"
  ]
}
```

方法二：通过 daemon.json 配置

- 本机使用 Administrator 账户为例，配置文件位于 C:\Users\Administrator\.docker\目录下的daemon.json

## Reference

1. https://blog.csdn.net/Lyon_Nee/article/details/124169099

2. https://zhuanlan.zhihu.com/p/347643668

3. https://segmentfault.com/a/1190000023117518

# 删除 ubuntu:latest 镜像，有以下几种方法：

镜像短ID：docker rmi 14f6；（这个代表镜像id以14f6开头的镜像，一般而言，前四位可以唯一标志，如果不可以，docker会提示的）
镜像长ID：docker rmi 14f60031763d；
镜像名： docker rmi ubuntu:latest；
镜像的digest：docker rmi > ubuntu@sha256:84c334414e2bfdcae99509a6add166bbb4fa4041dc3fa6af08046a66fed3005f。
以上的方法都能删除掉ubuntu:v1镜像。但日常生活中，我们比较常用的是短ID以及镜像名，因为用起来最方便。
删除多个镜像

我们可以使用 docker images -q来配合使用docker rmi，这样可以成批的删除希望删除的镜像。

docker images -q redis会输出所有仓库名为redis的镜像 id，所以如果想要删除所有仓库名为 redis 的镜像，可以这么写：

docker rmi $(docker images –q redis)

如果想要删除所有镜像，可以这么写：

docker rmi $(docker images –qa)



