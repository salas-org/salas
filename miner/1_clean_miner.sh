
MINER_ETH_DATA_PATH=$(pwd)/ethereum_data
MINER_SALAS_CONF_PATH=$(pwd)/salas_conf

if [ $CLEAN_MINER == "yes" ]; then
    echo "cleaning all miner data... hope you know what you're doing..."
else
    echo "skipping miner cleaning (since CLEAN_MINER in .env.cmds is not yes)"
    exit 0
fi

# removing data from chain
echo "removing $MINER_ETH_DATA_PATH"
rm -rf $MINER_ETH_DATA_PATH
mkdir $MINER_ETH_DATA_PATH

# cleanup the miner
mkdir -p $MINER_SALAS_CONF_PATH || true
echo -n "0x0" > $MINER_SALAS_CONF_PATH/node_address.txt
echo -n "0" > $MINER_SALAS_CONF_PATH/miner_address_registered.txt

exit 0