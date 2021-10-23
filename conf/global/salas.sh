#!/bin/bash

# salas network id 
NETWORKID=44404440
CHAINID=$NETWORKID

# bootnode for discovery
SALAS_ENODES="enode://891ff78928ad5b9c344862496aa924626222c84e9bb6b760de505d8b484107d66447e101eea6a9fef8cb8c1616550a77cb82fec6e21260054563459d683eacbf@51.15.202.74:30303" 
# add other bootnodes here, but leave the discport parameter off
# SALAS_ENODES="$SALAS_ENODES,"

# go-ethereum source code repo and commit
GETH_REPO="https://github.com/ethereum/go-ethereum.git"