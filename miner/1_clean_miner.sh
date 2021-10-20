
MINER_ETH_DATA_PATH=$(pwd)/ethereum_data
MINER_SALAS_CONF_PATH=$(pwd)/salas_conf

# need write on all directories for the deletes to succeed
read -p "This will remove all salas miner data from your system \nDo you want to continue? y/n [n] " yn
case $yn in
    [Yy]* ) ;;
    [Nn]* ) exit;;
    * ) exit;;
esac

# removing data from chain
echo "removing $MINER_ETH_DATA_PATH"
rm -rf $MINER_ETH_DATA_PATH
mkdir $MINER_ETH_DATA_PATH

# cleanup the miner
mkdir $MINER_SALAS_CONF_PATH || true
echo -n "0x0" > $MINER_SALAS_CONF_PATH/node_address.txt
echo -n "0" > $MINER_SALAS_CONF_PATH/miner_address_registered.txt