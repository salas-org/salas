# Build Geth in a stock Go builder container
FROM golang:1.16-alpine as builder

ARG gethrepo
RUN apk add --no-cache make gcc musl-dev linux-headers git patch
ENV ETHPATH="./ethereum"

# use this for a local version
# ADD $ETHPATH/src /go-ethereum
# use this for the git version
RUN git clone $gethrepo /go-ethereum

COPY ./install/local_install/consensus.patch /go-ethereum/consensus.patch
COPY ./install/local_install/protocol_params.patch /go-ethereum/protocol_params.patch

RUN patch --forward /go-ethereum/consensus/ethash/consensus.go < /go-ethereum/consensus.patch
RUN patch --forward /go-ethereum/params/protocol_params.go < /go-ethereum/protocol_params.patch

# change the default port 30303 to 31313 (skip the .github directory). It finds file and pipes them into sed for inplace replace
# -i ".bak" needed for macos
# LC_ALL=C set to C for utf-8 and ascii problems in sed (where gsed ignores these bytesequences)
RUN echo "replacing all occurences of default port number 30303 with 31313"

RUN for afile in $(grep --exclude "*.bak" -Rl 30303 /go-ethereum); do echo "found in file $afile, replacing with 31313"; sed -i.bak "s/30303/31313/g" $afile; rm $afile.bak || true; done

RUN cd /go-ethereum && make geth

# compile
#cd $ETHPATH/src
#export GOPATH=$ETHPATH
#go install ./...

# Pull Geth into a second stage deploy alpine container
FROM python:3.9-alpine

# get our modified geth
# COPY /cmd/geth /usr/local/bin/
COPY --from=builder /go-ethereum/build/bin/geth /salas/cmd/

RUN apk add --no-cache bash
RUN apk add --no-cache ca-certificates
#RUN apk update && apk add python3.9-dev gcc libc-dev
RUN apk add gcc libc-dev 

RUN pip install --upgrade pip setuptools
RUN pip install web3
RUN apk add git opensc

#RUN python3 -c "import solcx; solcx.install_solc('0.8.9')"

RUN git clone https://github.com/iamdefinitelyahuman/py-solc-x.git /py-solc-x
RUN cd /py-solc-x && python3 ./setup.py install
RUN cd /

RUN echo 'alias ll="ls -alsh"' >> /root/.profile

# copy the salas python code (the ethereum_data is not copied cause it is in the .dockerignore file)
ADD ./miner/ /salas/miner/
# copy the configuration (the ethereum_data is not copied cause it is in the .dockerignore file)
ADD ./conf/ /salas/conf/
ADD ./salas_contract/ /salas/salas_contract/

# for websocket
#EXPOSE 8545 8546 31313 31313/udp
# no websocket
EXPOSE 8545 31313 31313/udp

ENTRYPOINT ["/bin/bash"]
