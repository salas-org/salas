#!/bin/bash

# load configuration
source ../conf/0_load_conf.sh

LOCAL_ETH_DATA_PATH=$(pwd)/ethereum_data
LOCAL_SALAS_CONF_PATH=$(pwd)/salas_conf

VERBOSITY=3
LOCAL_PORT=30303
EXTRA_FLAGS="--nodiscover"

# run a mining node with an IPC via file geth.ipc in data directory 
echo "*******"
echo 'starting a node with this command:'
node_cmd="$GOPATH/bin/geth --nat none --datadir $LOCAL_ETH_DATA_PATH --syncmode full --verbosity $VERBOSITY --port $LOCAL_PORT --networkid $NETWORKID"
node_cmd="$node_cmd $EXTRA_FLAGS"
echo $node_cmd
$($node_cmd)