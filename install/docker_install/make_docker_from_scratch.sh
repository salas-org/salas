#!/bin/bash

currentdir=$(pwd)
source ../../conf/0_load_conf.sh

cd $SALAS_DIR
# adapt this line to suit your needs
docker build --build-arg gethrepo="$GETH_REPO" -t mytag1 -f ./install/docker_install/Dockerfile .
cd $currentdir