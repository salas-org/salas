
# load configuration
source ../conf/0_load_conf.sh

LOCAL_ETH_DATA_PATH=$(pwd)/ethereum_data
LOCAL_SALAS_CONF_PATH=$(pwd)/salas_conf
PASSWORD_FILE_PATH=$(pwd)/secrets/password.txt

# make a private-public key for the miner -> the private key is stored in the keystore file and protected with a password.
if test -f "$PASSWORD_FILE_PATH"; then
    echo "using password in $PASSWORD_FILE_PATH"
else
    mkdir -p $(pwd)/secrets
    echo "password file not found at $PASSWORD_FILE_PATH"
    echo -n "$PASSWORD" > $PASSWORD_FILE_PATH
    echo "saved password in $PASSWORD_FILE_PATH"
fi

if [ $INIT_MINER == "yes" ]; then
    echo "initializing miner data... hope you know what you're doing..."
else
    echo "skipping miner init (since INIT_MINER in .env.cmds is not yes)"
    exit 0
fi

output=$($SALAS_DIR/cmd/geth --datadir $LOCAL_ETH_DATA_PATH/ --password $PASSWORD_FILE_PATH account new)
address=$(echo "$output" | grep -i 'public address of the key' | tr -s ' ' | cut -d ' ' -f 6)
echo "Public miner address is $address"
mkdir -p "$LOCAL_SALAS_CONF_PATH" || true
echo -n "$address" > "$LOCAL_SALAS_CONF_PATH/node_address.txt"

# init the miner with the genesis file
$SALAS_DIR/cmd/geth --datadir $LOCAL_ETH_DATA_PATH init $SALAS_GLOBAL_CONF_PATH/genesis.json
