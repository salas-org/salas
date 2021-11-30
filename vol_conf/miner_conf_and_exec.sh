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
export SALAS_ENODES="enode://8c111ea8d3037c76b6e3a6196a830eb200f7ff753a2abdd7343174fbdd00bc81ae06ab6c1c999e0b5a5cff44c04a7ca300d2c1cd34dacda9bb0c33774182500a@51.159.184.213:31313"

/bin/bash -c "$@"