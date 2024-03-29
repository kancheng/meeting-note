# WSL

- https://learn.microsoft.com/zh-tw/windows/wsl/install-manual

```
docker pull nvidia/cuda:12.1.0-base-ubuntu22.04

docker run -it 2f9bc02xxxx /bin/bash

docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

## Reference

1. https://hub.docker.com/r/nvidia/cuda

2. https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/12.1.0/ubuntu2204/base/Dockerfile

3. https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md

4. https://medium.com/%E5%B7%A5%E7%A8%8B%E9%9A%A8%E5%AF%AB%E7%AD%86%E8%A8%98/docker-%E5%BB%BA%E7%AB%8B-cuda-%E5%8F%8A-cudnn-%E7%92%B0%E5%A2%83-2d0684b16df3

5. https://ithelp.ithome.com.tw/articles/10285253

6. https://docfunc.com/posts/27/%E5%9C%A8-windows-%E4%B8%AD%E5%AE%89%E8%A3%9D-wsl-2-post


# docker install on Ubuntu

- https://docs.docker.com/engine/install/ubuntu/

- ubuntu 中添加 daemon.json 文件

需要先创建文件:

```
sudo touch /etc/docker/daemon.json
```

然后编辑文件的内容，例如使用 Vim:

```
sudo vim /etc/docker/daemon.json
```

不需要像默认的那样使用“--config-file”选项指定该配置文件:

- https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file

```
{
    "registry-mirrors": [
        "https://registry.docker-cn.com"，
        "http://hub-mirror.c.163.com"，
    ]
}
```

文件配置完成后执行如下命令重新加载，并重启 docker

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```
- https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file


## Reference

1. https://blog.csdn.net/javaee_gao/article/details/121886577

2. https://blog.csdn.net/keyuhai/article/details/128663972

3. https://blog.csdn.net/qq_35427589/article/details/124822628

4. https://blog.csdn.net/u011700186/article/details/109452592

# docker 启动

启动 docker 并查看运行状态是否成功

```
## 启动docker
sudo systemctl start  docker
## 查看docker的状态
sudo systemctl status docker
## 重启docker
sudo systemctl restart docker
## 停止docker
sudo systemctl stop docker
## 查看所有正在运行容器
docker ps //
## containerId 是容器的ID
docker stop containerId
## 查看所有容器
docker ps -a
## 查看所有容器 ID
docker ps -a -q
## stop 停止所有容器
docker stop $(docker ps -a -q)
## remove 删除所有容器
docker rm $(docker ps -a -q)
## docker 的 service
systemctl status docker.service
```

# Dcoker hello-world

运行 docker 的 hello-world 案例

```
sudo docker run hello-world
```

# wsl start docker

```
sudo apt-get update
sudo apt-get install docker.io
```

- 純 linux 環境(不是在 windows 上啟動的，像是用蘋果電腦啟動的)

```
sudo systemctl start docker
```

- WSL 啟動

```
sudo dockerd
```

1. https://blog.csdn.net/LIFENG0402/article/details/117930091

2. https://ithelp.ithome.com.tw/articles/10310188

3. https://blog.csdn.net/LIFENG0402/article/details/117930091


# CUDA on WSL :: CUDA Toolkit Documentation

- https://docs.nvidia.com/cuda/wsl-user-guide/index.html

```
# 0. Installing WSL2
wsl.exe --install
wsl.exe --update

# 1. Update WSL Ubuntu
sudo apt-get update && sudo apt-get upgrade

# 2. Installing CUDA in WSL
sudo apt-key del 7fa2af80

wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin 48
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda-repo-wsl-ubuntu-11-6-local_11.6.2-1_amd64.deb 41
sudo dpkg -i cuda-repo-wsl-ubuntu-11-6-local_11.6.2-1_amd64.deb
sudo apt-key add /var/cuda-repo-wsl-ubuntu-11-6-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda-toolkit-11-6

# 2.1) Check, if Nvidia CUDA see videocard

nvidia-smi

# 3. Install Pip3
sudo apt install python3-pip
pip3 install --upgrade pip

# 4. Install TensorFlow
pip install tensorflow

# 4. Install CudNN
sudo apt-get install zlib1g
sudo dpkg -i ./cudnn-local-repo-ubuntu2004-8.4.1.50_1.0-1_amd64.deb
sudo cp /var/cudnn-local-repo-ubuntu2004-8.4.1.50/cudnn-local-E3EC4A60-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get install libcudnn8 libcudnn8-dev

# 4.1) Check TensorFlow:
# a) Check CPU:

python3 -c “import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))”

If tesor return, everything is working properly.

# б) Check GPU:

python3 -c “import tensorflow as tf; print(tf.config.list_physical_devices(‘GPU’))”

# If tesor return, everything is working properly.
```

## Reference

1. https://forums.developer.nvidia.com/t/windows-11-wsl2-cuda-windows-11-home-22000-708-nvidia-studio-driver-512-96/217721/3

# ubuntu-install-nvidia-drivers

- https://developer.nvidia.com/cuda-downloads

若有 Nvidia 顯示卡，Ubuntu 預設會載入開源的 nouveau 驅動，用指令 sudo lshw -C display 確認，driver 區段會顯示 "nouveau" 

```
sudo lshw -C display
```

欲使用 CUDA 技術，必須安裝專有的 Nvidia 驅動程式。先將 nouveau 套件刪除：

```
sudo apt update
sudo apt upgrade
sudo apt purge *nvidia*
```

接著使用 ubuntu-drivers list 指令列出目前 Nvidia 顯示卡可用的驅動版本。例如 GTX 1050Ti 會看到以下畫面，顯示卡若太舊可能就沒有新版驅動能裝。 

```
ubuntu-drivers list
```

按照輸出內容，填入要安裝的 Nvidia 驅動版本號。如果你沒有要使用 CUDA，那就挑最新版的裝；要使用 CUDA 請注意挑選正確的驅動版本。

## Reference

1. https://ivonblog.com/posts/ubuntu-install-nvidia-drivers/


