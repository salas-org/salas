#!/bin/bash

export NODE_CLEAN_DATA="no"
export NODE_INIT_ADDRESS="no"
export NODE_INIT_GENESIS="no"
export MINER_REGISTER_ADDRESS="no"
export FAUCET_START_SERVER="no"
export FAUCET_SALAS_PER_DROP="0.1"
export FAUCET_TIMEOUT_IN_SECS="86400"
export MINER_START_EID="no"
export CONTRACT_COMPILE_AND_DEPLOY="no"
export MINER_USE_3TH_PARTY_FOR_IP_ADDRESS="yes"
export VERBOSITY="4"
export RPC_OPTIONS=""
export SALAS_ENODES="none"

/bin/bash -c "$@"