# WSL

```
docker pull nvidia/cuda:12.1.0-base-ubuntu22.04

docker run -it 2f9bc027c2fba4266b2670d74769a2a5c87d2d3b6c4687b81c12d32017546f4f /bin/bash

docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

## Reference

1. https://hub.docker.com/r/nvidia/cuda

2. https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/12.1.0/ubuntu2204/base/Dockerfile

3. https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md

4. https://medium.com/%E5%B7%A5%E7%A8%8B%E9%9A%A8%E5%AF%AB%E7%AD%86%E8%A8%98/docker-%E5%BB%BA%E7%AB%8B-cuda-%E5%8F%8A-cudnn-%E7%92%B0%E5%A2%83-2d0684b16df3

5. https://ithelp.ithome.com.tw/articles/10285253