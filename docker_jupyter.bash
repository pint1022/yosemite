docker run --gpus all --rm -it --shm-size=512m -v $PWD/dataset:/workspace/dataset -v $PWD:/workspace/codes -v $PWD/logs:/workspace/logs \
    -w /workspace -p 0.0.0.0:6006:6006  -p 0.0.0.0:8888:8888   pint1022/tf-jupyter-tdfs-pandas:latest \
    jupyter lab --no-browser --allow-root --ip=0.0.0.0
# jupyter labextension list