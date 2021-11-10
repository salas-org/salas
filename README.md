# Salas

## Quickstart


## Install

The easiest solution to run a salas miner is to run a docker container. This won't work on macos
since the needed hypervisor on mac does not allow usb passthrough (needed for smartcard readers).
You can probably get it to run on macos based on the dockerfile and on the instructions below.

### Dockerfile

+ make a file with your secrets `cp .tmp.env.secrets .env.secrets` , and fill in the values for PIN and ID_CHAIN in the .env.secrets file. Tip: Do not use a space key around the equal sign.
+ `docker-compose build`
+ `docker-compose run` # this will start a container with your miner code
+ You should now copy your key to keep it save with `docker cp my_container_id:/salas/miner/ethereum_data/keystore ./keystore_backup`
+ For subsequent runs of your miner container, please use `docker-compose start` and `docker-compose stop`. You can check the state of your container with `docker ps -a`.

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

# LIcense info
## Salas License

All salas code is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), also included in our repository in the `COPYING` file.

## Ethereum License

Can be found at https://github.com/ethereum/go-ethereum/ . 