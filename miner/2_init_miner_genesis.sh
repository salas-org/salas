
# load configuration
source ../conf/0_load_conf.sh

LOCAL_ETH_DATA_PATH=$(pwd)/ethereum_data
LOCAL_SALAS_CONF_PATH=$(pwd)/conf
PASSWORD_FILE_PATH=$(pwd)/secrets/password.txt
MINER_KEYSTORE_PATH=$(pwd)/keystore

# make a private-public key for the miner -> the private key is stored in the keystore file and protected with a password.
if test -f "$PASSWORD_FILE_PATH"; then
    echo "using password in $PASSWORD_FILE_PATH"
else
    mkdir -p $(pwd)/secrets
    echo "password file not found at $PASSWORD_FILE_PATH"
    echo -n "$PASSWORD" > $PASSWORD_FILE_PATH
    echo "saved password in $PASSWORD_FILE_PATH"
fi

if [ $INIT_MINER_GENESIS == "yes" ]; then
    echo "initializing miner with genesis file ... hope you know what you're doing..."
else
    echo "skipping miner genesis init (since INIT_MINER_GENESIS in .env.cmds is not yes)"
    exit 0
fi

# init the miner with the genesis file
$SALAS_DIR/cmd/geth --keystore $MINER_KEYSTORE_PATH --datadir $LOCAL_ETH_DATA_PATH init $SALAS_GLOBAL_CONF_PATH/genesis.json
