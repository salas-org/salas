#!/bin/bash

export NODE_CLEAN_DATA="yes"
export NODE_INIT_ADDRESS="yes"
export NODE_INIT_GENESIS="yes"
export MINER_REGISTER_ADDRESS="no"
export FAUCET_START_SERVER="no"
export FAUCET_SALAS_PER_DROP="0.1"
export FAUCET_TIMEOUT_IN_SECS="86400"
export MINER_START_EID="yes"
export CONTRACT_COMPILE_AND_DEPLOY="no"
export MINER_USE_3TH_PARTY_FOR_IP_ADDRESS="yes"
export VERBOSITY="3"
export RPC_OPTIONS="--http --http.port 8545 --http.addr 0.0.0.0 --http.vhosts '*' --http.corsdomain 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn' --http.api eth,net,web3,personal --allow-insecure-unlock"
export SALAS_ENODES="enode://41cdc7595a8207e8d764372e5a0b127f21e09b5f9317dba6eaaefc9fca48fa92926ab4050225f297c81f4bc35db88472c7b54ba874ecd507e4e8284a77c20870@51.159.184.213:31313"

/bin/bash -c "$@"
