#!/bin/bash

# load configuration
source ../conf/0_load_conf.sh

MINER_ETH_DATA_PATH=$(pwd)/ethereum_data
MINER_SALAS_CONF_PATH=$(pwd)/salas_conf
PASSWORD_FILE_PATH=$(pwd)/password.txt
VERBOSITY=3
MINER_PORT=31343
MINER_GASPRICE_IN_GWEI=1

# get the address of node0 for unlocking the miner
coinbase=`cat $MINER_SALAS_CONF_PATH/node_address.txt`
echo "coinbase is $coinbase"

# run a mining node with an IPC via file geth.ipc in data directory 
echo "*******"
echo 'starting a miner with this command: (should NOT yet start mining)'
miner_cmd="$GOPATH/bin/geth --bootnodes $SALAS_ENODES --nat none --datadir $MINER_ETH_DATA_PATH --syncmode full --verbosity $VERBOSITY \
  --port $MINER_PORT --networkid $NETWORKID --miner.gasprice $MINER_GASPRICE_IN_GWEI --miner.etherbase "${coinbase}" \
  --unlock "${coinbase}" --password $PASSWORD_FILE_PATH --mine"
echo $miner_cmd
$($miner_cmd)