#!/bin/bash

# salas network id 
NETWORKID=44404440
CHAINID=$NETWORKID

# bootnode for discovery
# BOOTNODETCPPORT=30303
# BOOTNODEUDPPORT=30301
# dont add the discport
SALAS_ENODES="enode://01db36f194431efbac2969d7595ec980686cab53e6943fd63becfd43a2f61115406666e0992ab85cefb090890ca8203416819285203fec462f08367ff7a80127@127.0.0.1:30303" 
# add other bootnodes here
# BOOTNODES_ENODES="$BOOTNODES_ENODES,"

# go-ethereum source code repo and commit
GETH_REPO="https://github.com/ethereum/go-ethereum.git"