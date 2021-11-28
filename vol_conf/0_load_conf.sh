#!/bin/bash

# get the scripts directory
current_dir=$(pwd)
bash_source_path=$(dirname "${BASH_SOURCE}")

# main directory for salas
cd "$current_dir/$bash_source_path/.."
SALAS_DIR=$(pwd)
cd $current_dir

echo "found salas directory in $SALAS_DIR"

SALAS_GLOBAL_CONF_PATH="$SALAS_DIR/conf/global"
SALAS_LOCAL_CONF_PATH="$SALAS_DIR/conf/local"

source $SALAS_GLOBAL_CONF_PATH/salas.sh
source $SALAS_LOCAL_CONF_PATH/local.sh
