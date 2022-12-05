# ARG BASE_CONTAINER=tensorflow/tensorflow:latest-gpu-jupyter
ARG BASE_CONTAINER=nvcr.io/nvidia/tensorflow:22.10.1-tf2-py3
FROM $BASE_CONTAINER

USER root

RUN pip3 install tensorflow-datasets
RUN pip3 install tfds-nightly
RUN pip3 install pandas
# RUN pip3 install jupyterlab==3.2.0
# RUN pip3 install --upgrade "elyra[all]"
RUN pip3 install jupyter_http_over_ws jupyter-tensorboard  ipykernel nbformat
RUN jupyter serverextension enable --py jupyter_http_over_ws
RUN apt update
RUN apt -y upgrade
RUN apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt -y install nodejs
# RUN jupyter labextension install jupyterlab_tensorboard
RUN pip3 install git+https://github.com/cliffwoolley/jupyter_tensorboard.git