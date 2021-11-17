from logging import exception
from web3 import Web3
from pprint import pprint
import time
import subprocess
import pathlib as pl
import base64
import configparser

# this python program will output the signature (with your private key from an eid) of a previous block's hash (called key block)

IPC_PATH = '/salas/miner/geth.ipc'

config = configparser.ConfigParser()
config.read('../conf/global/salas.ini')
NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM = config.getint('key block', 'NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM')  # should never sign a block less that x blocks ago
NR_BLOCKS_TO_GO_BACK_TO_SIGN_MODULO = config.getint('key block', 'NR_BLOCKS_TO_GO_BACK_TO_SIGN_MODULO') # only consider the most recent block which is a multiple of this value (and which is not more recent than NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM)
config.read('../conf/local/eid.ini')
SIGN_KEY=config.get('beid', 'SIGN_KEY')
SIGN_METHOD=config.get('beid', 'SIGN_METHOD')
SECONDS_TO_SLEEP=config.getint('main', 'SECONDS_TO_SLEEP')
OFFSET=config.getint('main', 'OFFSET')

if os.environ['MINER_START_EID'] != 'yes':
    print("Not starting mining. Check the env.user file.")
    os.exit(0)

config.read('./secrets/secret.ini')
try:
    PIN=config.get('eid', 'PIN')
    ID_CHAIN=config.get('eid', 'ID_CHAIN')
except configparser.NoSectionError as err:
    # probably the secret.ini file does not exist 
    # let's try the env
    import os
    PIN=os.environ['PIN']
    ID_CHAIN=os.environ['ID_CHAIN']

def calc_block_to_sign(recent_block_nr: int) -> int:
    # get the block of which we need to sign the hash
    # first we subtract the NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM from the current block height
    # then we modulo the result and subtract the modulo to get a block number that is not so recent, but also not terribly old
    # the miner can find the same block using this algorithm 
    block_to_sign_nr = recent_block_nr + OFFSET
    if (recent_block_nr > NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM):
        # just to allow starting new blockchains
        block_to_sign_nr = recent_block_nr - NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM
    remainder = block_to_sign_nr % NR_BLOCKS_TO_GO_BACK_TO_SIGN_MODULO
    if block_to_sign_nr >= remainder:
        # just to allow starting new blockchains            
        block_to_sign_nr = block_to_sign_nr - remainder

    return block_to_sign_nr

def main():
    try:
        w3 = Web3(Web3.IPCProvider(IPC_PATH))
        # make sure the miner is started
        w3.geth.miner.start()    
    except FileNotFoundError as err:
        print(f"Couldn't find the IPC file at {IPC_PATH}")
        print("Was the miner started?")
        exit()

    last_signed_block_nr = -1
    past_recent_block_nr = -2
    nr_successive_failed_attempts = 0
        
    while (w3.isConnected()):

        # get the most recent block number
        recent_block_nr = w3.eth.get_block_number()
        if recent_block_nr != past_recent_block_nr:
            print(f"current block nr {recent_block_nr}, mining {recent_block_nr + OFFSET}")    

        # use an algo to get the block number that needs to be signed, then get the block
        block_to_sign_nr = calc_block_to_sign(recent_block_nr)
        if block_to_sign_nr == last_signed_block_nr:
            #print(f'previous signature of block still relevant. sleeping ...')
            pass
        else:
            print('previous signature to old')
            print(f"signing block {block_to_sign_nr}")

            # get the hash (in hex) of the block to sign
            block_to_sign = w3.eth.get_block(block_to_sign_nr)

            block_to_sign_hash=block_to_sign.hash
            block_to_sign_hex_hash=block_to_sign_hash.hex()

            # sign the hexadecimal hash, and retrieve the hexadeximal output
            print(f"signing block hash {block_to_sign_hex_hash} of block nr {block_to_sign_nr}")        
            signing_process_1 = subprocess.run([f"echo", '-n', f"{block_to_sign_hex_hash}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            signing_process_2 = subprocess.run(["pkcs11-tool", f"-p{PIN}", f"-d{SIGN_KEY}", "-s", f"-m{SIGN_METHOD}"], 
                                                input=signing_process_1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("signing_process_1 object: {}".format(signing_process_1.__dict__))
            signing_process_2_output = signing_process_2.stdout
            
            if signing_process_2.returncode == 0 :
                # signature was succesful, instruct the miner to use it as extradata
                # current signature length is 2048bits, adds up to 342 in base64
                # rounded up to 4 because of base64 padding == 344 bytes
                # the extra 8 bytes are used for the chain id (4 chars), and future provisioning
                signed_hash = signing_process_2_output.strip()
                signed_hash_base64 = base64.b64encode(signed_hash)
                print(f"len of signed hash is {len(signed_hash)}")
                print(f'base64 signed hash is {signed_hash_base64}')
                print(f"padding up to 352 len of base64 {signed_hash_base64.decode('ascii').ljust(352, '=')}")
                extradata_string = 'S001'
                extradata_string = extradata_string + '0000'
                extradata_string = extradata_string + signed_hash_base64.decode('ascii')
                extradata_string = extradata_string.ljust(352, "=")
                print(f"prefixing with id of the cert chain, and salas identifier {extradata_string}")
                
                w3.geth.miner.set_extra(extradata_string)
                last_signed_block_nr = block_to_sign_nr
                nr_successive_failed_attempts = 0

            else:
                signed_hash = '-1'
                nr_successive_failed_attempts = nr_successive_failed_attempts + 1
                print(f'signing hash failed')
                print(f'output was {signing_process_2_output}')

                if nr_successive_failed_attempts >= 5:
                    w3.geth.miner.stop()
                    input("Pausing since last couple of attempts failed. Press any key to continue retrying, and restart the miner.")
                    w3.geth.miner.start()
                    nr_successive_failed_attempts = 0

                print(f'retrying in {SECONDS_TO_SLEEP} seconds')

        # we can sleep for approx between calculation of a signed block nr and header
        time.sleep(SECONDS_TO_SLEEP)
        past_recent_block_nr = recent_block_nr

if __name__ == '__main__':
    main()