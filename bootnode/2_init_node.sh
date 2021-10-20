#!/bin/bash

# load configuration
source ../conf/0_load_conf.sh

MINER_ETH_DATA_PATH=$(pwd)/ethereum_data
MINER_SALAS_CONF_PATH=$(pwd)/salas_conf
PASSWORD_FILE_PATH=$(pwd)/password.txt

read -p "This could remove all salas miner data from your system \nDo you want to continue? y/n [n] " yn
case $yn in
    [Yy]* ) ;;
    [Nn]* ) exit;;
    * ) exit;;
esac

# make a private-public key for the miner -> the private key is stored in the keystore file and protected with a password. 
output=$($ETHPATH/bin/geth --datadir $MINER_ETH_DATA_PATH/ --password $PASSWORD_FILE_PATH account new)
address=$(echo "$output" | grep -i 'public address of the key' | tr -s ' ' | cut -d ' ' -f 6)
echo "Public miner address is $address"
echo "$address" > "$MINER_SALAS_CONF_PATH/miner_address.txt"

# init the miner with the genesis file
$ETHPATH/bin/geth --datadir $MINER_ETH_DATA_PATH init $SALAS_GLOBAL_CONF_PATH/genesis.json
