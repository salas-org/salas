# Salas

### TLDR;
Salas is Ethereum with an extra protocol aimed at decentralising mining power.

### What?
+ Salas is an Ethereum fork, much alike Binance Smart Chain
+ Salas requires miners to provide a proof of identity
+ Salas limits the rewards a single miner (a person) can accumulate over time

### Why? What's the problem we are trying to solve?
Salas aims at tackling two important problems with current proof-of-work chains. 
1. the decentralisation problem (part of the security, decentralisation, scalability blockchain trilemma) 
2. the ecological impact

Centralisation is problematic for trust in the blockchain (e.g. 51% attacks). It is caused by economies of scale, i.e. large scale actors can invest large sums in the necessary infrastructure and reap the benefits while smaller individual miners can not compete since they pay more for electricity and initial infrastructure while also having less stable returns.

This centralisation is a vicious circle. Centralisation leads to decreases in benefits for miners, and decreating benefits leads to more centralisation. This is a far cry from the initial view of a decentralized currency.

The centralisation and the economic incentives for larger actors to invest even more to maintain or increase their miner power also leads to much of the environmental impact that current proof-of-work blockchains have.

### Rationale behind the problem
Every blockchain needs some kind of bottleneck in order to choose which miner gets to sort the incoming transactions. 

In proof-of-work this bottleneck is hashing power. i.e. the more hashing power a miner has, the more often he will find a solution to a mathematical problem which proves he got 'lucky' and deserves the right to order the incoming transactions. The miner gets a rewards for doing this, otherwise no miner would ever do this work.

For other proof-of-something chains, the reasoning is similar. For instance, Chia needs a lot of fast storage, the more storage a miner has, the more often he gets 'lucky' and gets to reap the benefits.

This bottleneck ```X```, whether it is hashing power, or storage, or something else, should have a number of characteristics:
+ difficult to buy more of ```X```, or be difficult to scale (otherwise we scale to infinity, and consume all of it). In fact, it would be ideal if every miner would only have 1 unit of ```X```, and would be unable to accumulate more of ```X```.
+ for security, it would be beneficial if no miner would every lend out his ```X``` to other miners, or to pools.
+ it should not consume a lot of natural resources to operate ```X``` 
+ buying ```X``` should cost as little as possible
+ everyone should be able to own an ```X```
+ ```X``` should be interoperable with technology, e.g. your soul is not a good ```X```
+ should not contact or be dependant on a central service

It is clear that hashing power as ```X``` violates most of the above characteristics, like-wise for Chia, which led to a lot of wasted energy and misuse of hardware in both cases. But what other options do we have for ```X```?

### Solution
Salas uses proof-of-identity for miners as ```X```. The identified miners can only mine a certain number of blocks within a certain timeframe. It is not a permissioned blockchain as the miners can join the blockchain as long as they have access to a proof-of-identity. Currently Salas supports only the Belgian ID card as a basis for proving identity, but this will be expanded to other identity providers. This use a government issued proof-of-identity has the following characteristics:
+ almost impossible to buy/scale goverment issued cards/identity
+ since governmental issued identity/private keys typically have multiple usages, no miner will be incentivized to lend out his private keys, especially when the rewards are capped.
+ signing the block is done only when a proof-of-work has been found, so it consume very little energy. The proof-of-work only consumes a lot of energy when resources are centralised, which the use of proof-of-identity counters
+ a lot of habitants of our world already have proof-of-identity cards provided by their governments, or similar institutions.
+ not everyone has the ability to own a proof-of-identity, but it can be expected that the percentage of people that have access to this type of card will increase over the coming years.
+ it is a technological device, and a proof of concept is already operational, so it is interoperable with most chains based on proof-of-work, and probably other proof-of-something chains too.
+ an ID card is not dependant on a government, except for identity revocation lists. Currently, it is foreseen that the revocation lists will be read, cached an applied, but even without this use of revocation lists, it would be hard to scale the proof-of-identity especially since the identity contains typical registration numbers that are constant from one card to another for the same person. 

For this to work, the Salas protocol demands miners to provide some extra info in the ```extra-data``` field of their mined blocks, i.e. sign a recent validated block with their private key on the ID card, so that other miner can verify that the miner has access to their proof-of-identity in the form of an ID card. 

This does not impact anything else, so regular users of Salas do not need to provide any identity information, it is exactly like Ethereum for all other users, except for miners.

### Other similar efforts or reading material
https://consensys.net/blockchain-use-cases/digital-identity/
https://www.calctopia.com/papers/zk-PoI.pdf (a very similar effort? Is this only research or has it materialized?)

### Current state and roadmap


## Quickstart


## Install

The easiest solution to run a salas miner is to run a docker container. This won't work on macos since the needed hypervisor on mac does not allow usb passthrough (needed for smartcard readers). You can probably get it to run on macos based on the dockerfile and on the instructions below.

### Run a docker image with compose (easiest way)
+ make sure you have docker install. Follow the instruction on https://docs.docker.com/get-docker/ for your operating system if you need to install it.
+ make sure you have a working version of docker-compose https://docs.docker.com/compose/install/ .
+ make sure git is installed. More info on https://git-scm.com/ 
+ in a terminal type `git clone https://github.com/salas-org/salas.git`
+ cd in the salas directory with `cd salas`
+ make a file with your secrets `cp .tmp.env.secrets .env.secrets` , and fill in the values for PIN and ID_CHAIN in the .env.secrets file. Tip: Do not use a space key around the equal sign.
+ `docker-compose build` # this will take at least several coffees of time as it compiles the solidity compiler.
+ `docker-compose run` # this will start a container with your miner code`
+ For subsequent runs of your miner container, please use `docker-compose stop` and `docker-compose restart salas_miner`. You can check the state of your container with `docker-compose ps` or `docker ps -a`.
+ IMPORTANT: your personal keystore file can be found in the ./vol_keystore directory on the host. Copy this to a save place.

You can make a faucet if you want by setting START_FAUCET to yes in .env  

### Native on Linux

Execute the following commands on a standard ubuntu. First let's install the dependencies, then salas itself.

### Install the dependencies (tested on linux Ubuntu)

+ `apt update && apt -y upgrade`
+ `wget https://golang.org/dl/go1.17.2.linux-amd64.tar.gz`
+ `rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.2.linux-amd64.tar.gz  # deletes any previous golang install, so backup data if needed`
+ `export PATH=$PATH:/usr/local/go/bin`
+ `echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile`
+ `apt install python3-pip`
+ `pip install web3 py-solc-x`

### Install salas

+ `git clone https://github.com/salas-org/salas.git`
+ `cd salas/install/local_install`
+ `./1_clean_code.sh  # not needed on a first install` 
+ `./2_get_ethereum_and_patch_and_compile.sh`


## For developer
Starting a bootnode:

+ `cd bootnode`
+ `echo -n 'my_very_private_password' > password.txt
+ `./1_clean_node.sh`
+ `./2_init_node.sh`
+ `./3_start_node.sh`

This shoud have started a bootnode. The output shoud contain a line alike:
`enode://ab6583cb3b5c1248cbf0f7e9e377f2dd6c7fdebb6cb2e1e2d1659ce0621677d41c46f2fd9c354f42d62b76e00d085ed4209c575ee9858a90bf68fdba00f44af4@127.0.0.1:31313?discport=0`
substitute your public ip of your node for 127.0.0.1 and leave of the discport parameter, so you end up with:
`enode://ab6583cb3b5c1248cbf0f7e9e377f2dd6c7fdebb6cb2e1e2d1659ce0621677d41c46f2fd9c354f42d62b76e00d085ed4209c575ee9858a90bf68fdba00f44af4@51.15.202.74:31313`
This value can be added to the conf/global/salas.sh file to make your bootnode part of the salas network.
Make sure you setup a firewall rule to allow incoming tcp traffic on port 31313 (default port for salas). 

# List of ID CHAINS
'02' is for the Belgian ID - Authentication Key

# LIcense info
## Salas License

All salas code is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), also included in our repository in the `COPYING` file.

## Ethereum License

Can be found at https://github.com/ethereum/go-ethereum/ . 