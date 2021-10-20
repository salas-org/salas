
source ../conf/0_load_conf.sh

# removing data from chain
echo "pulling geth (go-ethereum) to $ETHPATH"
git clone $GETH_REPO $ETHPATH/src

# patch
patch $ETHPATH/src/consensus/ethash/consensus.go < ./consensus.patch
patch $ETHPATH/src/params/protocol_params.go < ./protocol_params.patch

# compile
cd $ETHPATH/src
export GOPATH=$ETHPATH
go install ./...