
MINER_ETH_DATA_PATH=$(pwd)/ethereum_data
MINER_SALAS_CONF_PATH=$(pwd)/conf
MINER_KEYSTORE_PATH=$(pwd)/keystore

if [ $NODE_CLEAN_DATA == "yes" ]; then
    echo "cleaning all miner data... hope you know what you're doing..."
else
    echo "skipping miner cleaning (since NODE_CLEAN_DATA in .env.cmds is not yes)"
    exit 0
fi

# removing data from chain
echo "removing $MINER_ETH_DATA_PATH"
rm -rf $MINER_ETH_DATA_PATH
mkdir $MINER_ETH_DATA_PATH

# NOT removing the keystore, that should be done from the host machine in the mounted volume
echo "NOT removing the keystore at $MINER_KEYSTORE_PATH, you need to do this manually if needed"

# cleanup the miner
echo "NOT removing the conf (node_address and whether it is registered), you need to do this manually if needed"
# mkdir -p $MINER_SALAS_CONF_PATH || true
# echo -n "0x0" > $MINER_SALAS_CONF_PATH/node_address.txt
# echo -n "0" > $MINER_SALAS_CONF_PATH/miner_address_registered.txt

exit 0