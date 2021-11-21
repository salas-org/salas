#!/bin/bash

# salas network id 
NETWORKID=44404440
CHAINID=$NETWORKID
TCP_DEFAULT_PORT_SALAS=31313   

# bootnode for discovery
SALAS_ENODES="enode://3f6bba44c87991a5ece92ad53a588e0ba8d706fff49bdb2bb19801af2d1153364b7920309ed847226ba58ea553505c4e1c0d9b52f17c77185e6c71421adac702@51.159.184.213:31313" 
# add other bootnodes here, but leave the discport parameter off
# SALAS_ENODES="$SALAS_ENODES,"

# go-ethereum source code repo and commit
GETH_REPO="https://github.com/ethereum/go-ethereum.git"