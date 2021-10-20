
LOCAL_ETH_DATA_PATH=$(pwd)/ethereum_data
LOCAL_SALAS_CONF_PATH=$(pwd)/salas_conf

# need write on all directories for the deletes to succeed
read -p "This will remove all salas data for this node from your system. Do you want to continue? y/n [n] " yn
case $yn in
    [Yy]* ) ;;
    [Nn]* ) exit;;
    * ) exit;;
esac

# removing data from chain
echo "removing $LOCAL_ETH_DATA_PATH"
rm -rf $LOCAL_ETH_DATA_PATH
mkdir $LOCAL_ETH_DATA_PATH || true

# cleanup the node address
echo "removing node address"
echo -n "0x0" > $LOCAL_SALAS_CONF_PATH/node_address.txt