#!/bin/bash

# main directory for salas
SALAS_DIR="$(cd .. && pwd)"
SALAS_GLOBAL_CONF_PATH="$SALAS_DIR/conf/global"
SALAS_LOCAL_CONF_PATH="$SALAS_DIR/conf/local"

source $SALAS_GLOBAL_CONF_PATH/salas.sh
source $SALAS_LOCAL_CONF_PATH/local.sh
