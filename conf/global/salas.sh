#!/bin/bash

# salas network id 
NETWORKID=44404440
CHAINID=$NETWORKID

# bootnode for discovery
SALAS_ENODES="enode://ab6583cb3b5c1248cbf0f7e9e377f2dd6c7fdebb6cb2e1e2d1659ce0621677d41c46f2fd9c354f42d62b76e00d085ed4209c575ee9858a90bf68fdba00f44af4@51.15.202.74:30303" 
# add other bootnodes here, but leave the discport parameter off
# SALAS_ENODES="$SALAS_ENODES,"

# go-ethereum source code repo and commit
GETH_REPO="https://github.com/ethereum/go-ethereum.git"