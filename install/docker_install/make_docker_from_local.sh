#!/bin/bash

currentdir=$(pwd)
source ../../conf/0_load_conf.sh

cd $SALAS_DIR
# adapt this line to suit your needs
docker build -t mytag1 -f $SALAS_DIR/install/docker_install/Dockerfile.from_local .
cd $currentdir