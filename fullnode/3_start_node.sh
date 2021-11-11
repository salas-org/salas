#!/bin/bash

# load configuration
source ../conf/0_load_conf.sh

LOCAL_ETH_DATA_PATH=$(pwd)/ethereum_data
LOCAL_SALAS_CONF_PATH=$(pwd)/conf
MINER_IPC_PATH=$(pwd)/geth.ipc

VERBOSITY=3
LOCAL_PORT=31323
#EXTRA_FLAGS="--nodiscover --http --http.api eth,net,web3,personal --http.corsdomain '*' "
# this is probably not yet secure
EXTRA_FLAGS="--http --http.api eth,net,web3,personal --http.corsdomain '*' "

# run a node with an IPC via file geth.ipc in data directory 
echo "*******"
echo 'starting a node with this command:'
node_cmd="$GOPATH/bin/geth --ipcpath $MINER_IPC_PATH --bootnodes $SALAS_ENODES --nat none --datadir $LOCAL_ETH_DATA_PATH --syncmode full --verbosity $VERBOSITY --port $LOCAL_PORT --networkid $NETWORKID"
node_cmd=$node_cmd $EXTRA_FLAGS
echo $node_cmd
$($node_cmd)
