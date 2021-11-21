#!/bin/bash

# salas network id 
NETWORKID=44404440
CHAINID=$NETWORKID
TCP_DEFAULT_PORT_SALAS=31313   

# bootnode for discovery
SALAS_ENODES="enode://6b609d8fda9b3de63f7769a6ded9820902c401b17abe625e623e89398a164a74c9e30c222fcd46f201f2717260dd456293943c93782a25367d21f79d18cf90d8@51.159.184.213:31313" 
# add other bootnodes here, but leave the discport parameter off
# SALAS_ENODES="$SALAS_ENODES,"

# go-ethereum source code repo and commit
GETH_REPO="https://github.com/ethereum/go-ethereum.git"