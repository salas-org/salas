source ../conf/0_load_conf.sh

TCP_DEFAULT_PORT_ETHEREUM=30303

# removing data from chain
echo "pulling geth (go-ethereum) to $ETHPATH"
git clone $GETH_REPO $ETHPATH/src

# patch
patch $ETHPATH/src/consensus/ethash/consensus.go < ./consensus.patch
patch $ETHPATH/src/params/protocol_params.go < ./protocol_params.patch

# change the default port 30303 to 31313 (skip the .github directory). It finds file and pipes them into sed for inplace replace
# -i ".bak" needed for macos
# LC_ALL=C set to C for utf-8 and ascii problems in sed (where gsed ignores these bytesequences)
echo "replacing all occurences of default port number $TCP_DEFAULT_PORT_ETHEREUM with $TCP_DEFAULT_PORT_SALAS"

for afile in $(grep --exclude "*.bak" -Rl "$TCP_DEFAULT_PORT_ETHEREUM" $ETHPATH/src)
do
	echo "found in file $afile, replacing with $TCP_DEFAULT_PORT_SALAS"
    sed -i.bak "s/$TCP_DEFAULT_PORT_ETHEREUM/$TCP_DEFAULT_PORT_SALAS/g" $afile
    rm $afile.bak || true
done

# compile
cd $ETHPATH/src
export GOPATH=$ETHPATH
go install ./...