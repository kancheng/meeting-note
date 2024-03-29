# Conda

檢查目前版本

```
conda –V
```

建立虛擬環境

```
conda env list
```

建立名為 myenv 的虛擬環境，並且是安裝python 3.5的版本，那可鍵入下面的命令

```
conda create --name myenv python=3.5
```

列出目前虛擬環境狀況

```
conda env list
```

啟動虛擬環境

```
conda activate myenv
```

刪除整個虛擬環境，則可輸入下面命令即可完成刪除

```
conda env remove --name myenv
```

## 改变 conda 虚拟环境的默认路径

用户目录下的.condarc文件（C:\Users\username）

1. 打开.condarc文件之后，添加或修改.condarc 中的 env_dirs 设置环境路径，按顺序第⼀个路径作为默认存储路径，搜索环境按先后顺序在各⽬录中查找。直接在.condarc添加：

```
envs_dirs:
  - D:\Anaconda3\envs
```
2. 在 Anaconda Promp 执行命令：

```
conda config --add envs_dirs newdir #增加环境路径newdir
```

## install

```
pip install -r .\requirements.txt
```

## Reference

1. https://medium.com/python4u/%E7%94%A8conda%E5%BB%BA%E7%AB%8B%E5%8F%8A%E7%AE%A1%E7%90%86python%E8%99%9B%E6%93%AC%E7%92%B0%E5%A2%83-b61fd2a76566

2. https://www.jb51.net/article/256139.htm

3. https://blog.csdn.net/weixin_42519126/article/details/113680660


