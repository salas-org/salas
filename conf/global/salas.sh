#!/bin/bash

# salas network id 
NETWORKID=44404440
CHAINID=$NETWORKID
TCP_DEFAULT_PORT_SALAS=31313   

# bootnode for discovery
SALAS_ENODES="enode://41561e4a3cd2ff2028b274f7458259895382baa42ff56fcbcb9de690f647758d17e9e9c80eff7d6d444e547e6ab63fed2ab18ade64d092f3371ce1b5927df9b1@51.159.184.213:31313" 
# add other bootnodes here, but leave the discport parameter off
# SALAS_ENODES="$SALAS_ENODES,"

# go-ethereum source code repo and commit
GETH_REPO="https://github.com/ethereum/go-ethereum.git"