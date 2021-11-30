import os, sys
import configparser
from web3 import Web3
from solcx import compile_source
import subprocess
import pprint

IPC_PATH = './geth.ipc'
CONTRACT_PATH = '../salas_contract'

if os.environ['MINER_REGISTER_ADDRESS'] != 'yes':
    print("Skipping address registration.")
    sys.exit(0)

config = configparser.ConfigParser()
config.read('../conf/global/salas.ini')
SALAS_CONTRACT_ADDRESS = config.get('main', "SALAS_CONTRACT_ADDRESS")
SALAS_CONTRACT_COST = config.get('main', 'SALAS_CONTRACT_COST')
config.read('../conf/local/eid.ini')
SIGN_KEY=config.get('beid', 'SIGN_KEY')
SIGN_METHOD=config.get('beid', 'SIGN_METHOD')

config.read('./secrets/secret.ini')
try:
    PIN=config.get('eid', 'PIN')
    ID_CHAIN=config.get('eid', 'ID_CHAIN')
except configparser.NoSectionError as err:
    # probably the secret.ini file does not exist 
    # let's try the env
    PIN=os.environ['PIN']
    ID_CHAIN=os.environ['ID_CHAIN']

with open('./secrets/password.txt') as f:
    account_password = f.read()
with open('./conf/node_address.txt') as f:
    miner_address = f.read()

with open(f'{CONTRACT_PATH}/salas_contract.sol') as f:
    solidity_code = f.read()

def w3_provider(w3=Web3(Web3.IPCProvider(IPC_PATH))):
    # little hack: default parameter are only evaluated once by the interpreter
    return w3

def get_latest_event_from_address_to_contract(topic_from_address, w3=w3_provider()):

    w3 = w3_provider()

    # get the contract, bytecode and ABI
    compiled_sol = compile_source(solidity_code)
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']

    salas = w3.eth.contract(address=SALAS_CONTRACT_ADDRESS, abi=abi)
    salas_event = salas.events.RegisteredAddress()

    # find the latest event
    event_signature_hash = w3.keccak(text="RegisteredAddress(address,string,string,string)").hex()
    event_filter = w3.eth.filter({
        "fromBlock": 0,
        "address": SALAS_CONTRACT_ADDRESS,
        "topics": [event_signature_hash,
                topic_from_address],  #from address == miner address
        })
    events = event_filter.get_all_entries()
    #print(f"retrieved {len(events)} event log entries from the contract and for this miner")

    # decode the data of the last event (is it always the last in time?)
    if len(events) == 0:
        raise ValueError("No link found between public key and keccak256 ethereum address. Did you register the address?")

    event = events[-1]
    event_data = event.data
    event_decoded = salas_event.processLog(event)
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
    return event_decoded

def retrieve_public_certificate():
    # get the user certificate for this key id on the card
    # TODO: check that it is a authentication (and not a signing key)
    # TODO: check that the chain id is correct for the certificate

    user_cert = ''

    if not(os.path.isfile('./cert.pem')):
        with open('./cert.pem', "w") as f:
            print(f"retrieving use certificate and converting to pem format")
            # pkcs11-tool --pin 1234 --read-object --id 02 --type cert --output-file cert.der
            print(f"storing user certificate")  
            signing_process_1 = subprocess.run(["pkcs11-tool", f"-p{PIN}", 
                                                "--read-object", "--type", "cert", "--id", f"{SIGN_KEY}"], 
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # pipe the DER certificate in openssl to convert it to pem
            # openssl x509 -inform DER  -outform PEM
            signing_process_2 = subprocess.run(["openssl", "x509", 
                                                "-inform", "DER", "-outform", "PEM", ">"], 
                                                input=signing_process_1.stdout, 
                                                stdout=f, stderr=subprocess.PIPE)

            print(f"retrieved hex output")
            if signing_process_2.returncode == 0 :
                print(f"user certificate stored in file cert.pem")                                    
            else:
                print(f'user certificate could not be found, and could not be retrieved from smart card')
                raise ValueError
    
    # lets read the certificate
    with open("./cert.pem") as f:
            user_cert = f.read()
    return user_cert

def main():

    # get web3.py instance, and unlock the default account
    try:
        w3 = w3_provider()
        w3.geth.personal.unlock_account(miner_address, account_password, 600)
        print(f'miner address is {miner_address}')
        print(f'current balance on address is {w3.eth.get_balance(miner_address)}')
    except FileNotFoundError as err:
        print("Can't connect to your IPC / server")
        raise err

    # get the contract, bytecode and ABI
    compiled_sol = compile_source(solidity_code)
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']

    ###################
    # execute functions on the contract 
    ###################
    salas_contract = w3.eth.contract(address=SALAS_CONTRACT_ADDRESS, abi=abi)

    # call a view
    cost_in_wei = salas_contract.functions.getCost().call()
    print(cost_in_wei)

    ###################
    # sanity checks
    ###################
    # latest_event = get_latest_event_from_address_to_contract(miner_address[2:])
    # if len(latest_event) != 0:
    #     print("assuming this address is already registered")
    #     exit(0)

    # do we already have an certificate file?
    print("retrieving user certificate")
    user_pem_cert = retrieve_public_certificate()
    print(type(user_pem_cert))
    user_pem_cert = user_pem_cert.splitlines()
    user_pem_cert_inner = "".join(user_pem_cert[1:-1])
    print("user certificate loaded")

    if w3.eth.get_balance(miner_address) < float(SALAS_CONTRACT_COST):
        print("the account's balance is insufficient to cover registration costs")
        print("use the faucet to request some salas in order to cover the transaction fees")
        exit(0)

    # calculate the signature of the address of the client/miner
    # TODO: get from environment and check the stdout from the subprocess
    print(f"signing miner address {miner_address} with private key ")
    signing_process_1 = subprocess.run([f"cat", "./conf/miner_address.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    signing_process_2 = subprocess.run(["pkcs11-tool", f"-p{PIN}", f"-d{SIGN_KEY}", "-s", f"-m{SIGN_METHOD}"], 
                                        input=signing_process_1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"signing...")                                    
    signing_process_2_output = signing_process_2.stdout.hex()
    print(f"retrieved hex output")
    if signing_process_2.returncode == 0 :
        signed_address = signing_process_2_output
        print(f'signed address is {signed_address}')

    else:
        print(f'signing address failed')
        print(f'output was {signing_process_2_output}')
        quit()

    # call a transactions / change the state on the blockchain
    tx_hash = salas_contract.functions.registerAddress(ID_CHAIN
                                    , user_pem_cert_inner
                                    , signed_address).transact({
                                        'from': miner_address,
                                        'to': SALAS_CONTRACT_ADDRESS,
                                        'value': int(SALAS_CONTRACT_COST)
                                    })
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Transaction receipt mined:")
    pprint.pprint(dict(tx_receipt))
    print("\nWas transaction successful?")
    pprint.pprint(tx_receipt["status"])

    with open("./conf/miner_address_registered.txt", "w") as f:
        f.write("1")

if __name__ == '__main__':
    main()