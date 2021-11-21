
# load configuration
source ../conf/0_load_conf.sh

MINER_ETH_DATA_PATH=$(pwd)/ethereum_data
MINER_KEYSTORE_PATH=$(pwd)/keystore
MINER_SALAS_CONF_PATH=$(pwd)/conf
MINER_IPC_PATH=$(pwd)/geth.ipc
MINER_ETHASH_PATH=$(pwd)/ethash
PASSWORD_FILE_PATH=$(pwd)/secrets/password.txt
MINER_PORT=31313
MINER_GASPRICE_IN_GWEI=1

# check if we have a keystore file else do a init of the miner
# look for empty dir
if [ -d "$MINER_KEYSTORE_PATH" ]
then
	if [ "$(ls -A $MINER_KEYSTORE_PATH/UTC*)" ]; then
     echo "keystore found"
	else
    echo "$MINER_KEYSTORE_PATH is Empty"
    echo "initializing miner"
    INIT_MINER='yes'
    ./2_init_miner.sh
	fi
else
  echo "Directory $MINER_KEYSTORE_PATH not found."
  echo "initializing miner"  
  INIT_MINER='yes'
  ./2_init_miner.sh
fi

# get the address of node0 for unlocking the miner
coinbase=`cat $MINER_SALAS_CONF_PATH/node_address.txt`
echo "coinbase is $coinbase"

# run a mining node with an IPC via file geth.ipc in data directory 
echo "*******"
echo 'starting a miner with this command: (should NOT yet start mining)'

# TODO: yes yes, very insecure
EXTRA_PARAMS=""
if [[ $MINER_USE_3TH_PARTY_FOR_IP_ADDRESS == "yes" ]]; then
    EXTRA_PARAMS="$EXTRA_PARAMS --nat extip:$(curl https://ipinfo.io/ip)"
fi

# If the enodes parameter is longer than x chars, use it as bootnodes, else disregard it
if [[ ${#SALAS_ENODES} -gt 8 ]] ; then
    BOOTNODES_PARAMS="--bootnodes $SALAS_ENODES"
else
    BOOTNODES_PARAMS="--nodiscover"
fi


miner_cmd="$SALAS_DIR/cmd/geth --ipcpath $MINER_IPC_PATH --keystore $MINER_KEYSTORE_PATH \
  --datadir $MINER_ETH_DATA_PATH --syncmode full \
  --verbosity $VERBOSITY --port $MINER_PORT --networkid $NETWORKID \
  --miner.gasprice $MINER_GASPRICE_IN_GWEI --miner.etherbase ${coinbase} \
  --unlock ${coinbase} --password $PASSWORD_FILE_PATH --mine $EXTRA_PARAMS \
  --syncmode full --ethash.dagdir=$MINER_ETHASH_PATH --light.serve 30 \
  $BOOTNODES_PARAMS"

echo $miner_cmd
$($miner_cmd)