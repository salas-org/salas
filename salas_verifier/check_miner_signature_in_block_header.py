from logging import exception
from web3 import Web3
from solcx import compile_source
import argparse
import OpenSSL
from six import u, b, binary_type, PY3
import subprocess
import sys
import base64
import re
import configparser
from cert_chains.cc_mapping import chain_id_mappings as cc_map


#############
# given a miner address, this python program check whether it the address is linked to a public certificate that can be verified using the known chains
# and also checks whether the corresponding private key was used to sign the address of the miner 
#############

IPC_PATH = '../miner/ethereum_data/geth.ipc'
PATH_ = '../salas_contract'

config = configparser.ConfigParser()
config.read('../conf/global/salas.ini')
SALAS_CONTRACT_ADDRESS=config.get('main', 'SALAS_CONTRACT_ADDRESS')
NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM = config.getint('key block', 'NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM')  # should never sign a block less that x blocks ago
NR_BLOCKS_TO_GO_BACK_TO_SIGN_MODULO = config.getint('key block', 'NR_BLOCKS_TO_GO_BACK_TO_SIGN_MODULO') # only consider the most recent block which is a multiple of this value (and which is not more recent than NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM)

CONTRACT_DEPLOYED = PATH_ + '/salas_conf/contract_deployed.txt'
CONTRACT_PATH= PATH_ + '/salas_contract.sol'
SLACK_ON_OFFSET_FOR_KEYBLOCK = 4

with open(CONTRACT_DEPLOYED) as f:
    contract_deployed = f.read()

# Instantiate the parser
parser = argparse.ArgumentParser(description='Python program to check if the miner is okay')

# Required positional arguments: etherbase of the miner, chain_id, public key, recent header nr, signed recent header,
parser.add_argument('etherbase', type=ascii, help='The etherbase of the miner that send the block to be validated')
parser.add_argument('mined_block_nr', type=int, help='The number of the block that need to be validated')
parser.add_argument('mined_block_extradata', type=ascii, help='A signed header (in extradata) of the block that needs to be validated')

def calc_block_to_sign(recent_block_nr: int) -> int:
    # get the block of which we need to sign the hash
    # first we subtract the NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM from the current block height
    # then we modulo the result and subtract the modulo to get a block number that is not so recent, but also not terribly old
    # the miner can find the same block using this algorithm 
    block_to_sign_nr = recent_block_nr
    if (recent_block_nr > NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM):
        # just to allow starting new blockchains
        block_to_sign_nr = recent_block_nr - NR_BLOCKS_TO_GO_BACK_TO_SIGN_MINIMUM
    remainder = block_to_sign_nr % NR_BLOCKS_TO_GO_BACK_TO_SIGN_MODULO
    if block_to_sign_nr >= remainder:
        # just to allow starting new blockchains            
        block_to_sign_nr = block_to_sign_nr - remainder

    return block_to_sign_nr

def w3_provider(ipc_path=IPC_PATH):
    return Web3(Web3.IPCProvider(ipc_path))

def ethereum_handler(w3, other_miner_etherbase, mined_block_nr, signed_key_block_hash):
    
    # test to see if we already have a salas contract
    # if not than just return okay
    if contract_deployed != '1' or mined_block_nr<=130:
        print("contract not yet deployed? or header block nr small")
        return 0

    # get the contract, bytecode and ABI
    with open(CONTRACT_PATH) as f:
        solidity_code = f.read()
    compiled_sol = compile_source(solidity_code)
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']

    ###################
    # Check whether the public certificate is valid given the known intermediate and root certificate
    ###################
    salas = w3.eth.contract(address=SALAS_CONTRACT_ADDRESS, abi=abi)
    salas_event = salas.events.RegisteredAddress()

    # get the events from the transaction from the etherbase to the salas contract address
    # address = 0x65219b02605c8C6A0451f621D7898D7354dFe86b
    # event RegisteredAddress(address indexed senderAddress, string id_chain, string public_key, string signed_address);
    
    # WORKING
    other_miner_etherbase = other_miner_etherbase[3:-1]  #is enclosed in '0x ....'  (including the quotes)
    topic_from_address = '0x000000000000000000000000' + other_miner_etherbase
    print(f"verifying block from miner with etherbase {topic_from_address}")

    event_signature_hash = w3.keccak(text="RegisteredAddress(address,string,string,string)").hex()
    event_filter = w3.eth.filter({
        "fromBlock": 0,
        "address": SALAS_CONTRACT_ADDRESS,
        "topics": [event_signature_hash,
                topic_from_address],  #from address == miner address
        })
    events = event_filter.get_all_entries()
    print(f"retrieved {len(events)} event log entries from the contract and for this miner")

    # decode the data of the last event (is it always the last in time?)
    if len(events) == 0:
        raise ValueError("No link found between public key and keccak256 ethereum address. Did you register the address?")

    event = events[-1]
    event_data = event.data
    event_decoded = salas_event.processLog(event)
    print(event_decoded)
    # data in event
    # event_decoded.args.senderAddress
    # event_decoded.args.id_chain
    # event_decoded.args.public_key_certificate
    # event_decoded.args.signed_address
    # event_decoded.event
    # event_decoded.logIndex
    # event_decoded.transactionIndex
    # event_decoded.transactionHash
    # event_decoded.address
    # event_decoded.blockHash
    # event_decoded.blockNumber
    
    # get the public key, get the id_chain, make the complete certificate chain
    chain_id = event_decoded.args.id_chain
    chain = cc_map[chain_id]

    end_entity_cert = chain["end_entity_cert_template"].format(cert_with_pk_to_verify=event_decoded.args.public_key_certificate)
    #end_entity_cert = bytes(end_entity_cert, 'utf-8')

    intermediate_certs = chain["intermediate_certs"]['citizen']
    root_cert = chain["root"]
        
    # way of working to verify a personal certificate:
    # First trust root, then check intermediate, then trust intermediate, then check personal certificate
    parsed_root = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, root_cert)
    parsed_chain = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, intermediate_certs)
    parsed_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, end_entity_cert)

    # trust root
    print("trusting root certificate")
    store = OpenSSL.crypto.X509Store()
    store.add_cert(parsed_root)

     # only add intermediate if it can be verified by the root
    print("verifying intermediate certificate")
    store_ctx = OpenSSL.crypto.X509StoreContext(store, parsed_chain)
    store_ctx.verify_certificate()
    store.add_cert(parsed_chain)
    
    # Now check the end-entity certificate.
    print("verifying end user certificate")
    store_ctx = OpenSSL.crypto.X509StoreContext(store, parsed_cert)
    try:
        store_ctx.verify_certificate()
    except OpenSSL.crypto.X509StoreContextError as err:
        print("Could not validate the certificates for the given address")
        raise err 

    print(f"end user certificate verified using chain id: {chain_id}")

    ###################
    # Check whether the corresponding private key was used to sign the miner's keccak256 address
    ###################

    hex_signature = event_decoded.args.signed_address
    bytes_signature = bytes.fromhex(hex_signature)

    try:
        OpenSSL.crypto.verify(parsed_cert
            , bytes_signature
            , '0x' + other_miner_etherbase, 
            'sha1')

    except Exception as err:
        print('Could not verify the signature of the keccak256_address with the linked public key')
        raise err

    print(f"private key used to sign the address corresponds to the public key in the certificate")

    ###################
    # Check whether the mined block extradata is the key block hash that is signed by the same private key
    ###################

    signed_key_block_hash_base64 = signed_key_block_hash.encode('ascii')
    signed_key_block_hash_bytes = base64.b64decode(signed_key_block_hash_base64)

    succes_key_block = False
    succes_key_block_with_offset = False

    try:
        # Get the hex(base64(sign(hex(hash of the key block))))
        mined_key_block_nr_ideally = calc_block_to_sign(mined_block_nr)
        mined_key_block_hash_in_hex_ideally = w3.eth.get_block(mined_key_block_nr_ideally).hash.hex()

        OpenSSL.crypto.verify(parsed_cert
            , signed_key_block_hash_bytes
            , mined_key_block_hash_in_hex_ideally, 
            'sha1')
        succes_key_block = True

    except Exception as err:
        print('Could not verify the signature of the supposedly signed key block hash with the linked public key')

    try:
        # Sometimes the miner will get it wrong, and we should give a little slack if it is close to the key block jump
        # The reason is that the extra_data is updated async and injected into the miner, but the latter could have mined a number of blocks in the meantime
        if calc_block_to_sign(mined_block_nr-SLACK_ON_OFFSET_FOR_KEYBLOCK) != calc_block_to_sign(mined_block_nr):

            # Get the hex(base64(sign(hex(hash of the key block))))
            mined_key_block_nr_ideally = calc_block_to_sign(mined_block_nr-SLACK_ON_OFFSET_FOR_KEYBLOCK)
            mined_key_block_hash_in_hex_ideally = w3.eth.get_block(mined_key_block_nr_ideally).hash.hex()

            OpenSSL.crypto.verify(parsed_cert
                , signed_key_block_hash_bytes
                , mined_key_block_hash_in_hex_ideally, 
                'sha1')
            succes_key_block_with_offset = True
                
    except Exception as err:
        print('Could not verify the signature of the supposedly signed key block hash (2nd try with the previous key block) with the linked public key')
        
    if (succes_key_block == False) and (succes_key_block_with_offset == False):
        raise OpenSSL.crypto.Error

    print(f"the extradata of the mined block is indeed the hash of a previous key block that was signed with the private key of the miner")

def main():

    # parse arguments to main
    args = parser.parse_args()
    etherbase = args.etherbase
    mined_block_nr = int(args.mined_block_nr)
    signed_key_block_hash_in_base64 = args.mined_block_extradata
    
    ethereum_handler(w3_provider(), etherbase, mined_block_nr, signed_key_block_hash_in_base64)

    sys.stdout.write('{"result": "verification succesful"}\n')
    sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    main()
