from web3 import Web3
from solcx import compile_source
import subprocess
import pprint
from configparser import ConfigParser

IPC_PATH = './ethereum_data/geth.ipc'
CONTRACT_PATH = '../salas_contract'

config = ConfigParser()
config.read('../conf/global/salas.ini')
SALAS_CONTRACT_ADDRESS = config.get('main', "SALAS_CONTRACT_ADDRESS")
SALAS_CONTRACT_COST = config.get('main', 'SALAS_CONTRACT_COST')
config.read('../conf/local/eid.ini')
SIGN_KEY=config.get('beid', 'SIGN_KEY')
SIGN_METHOD=config.get('beid', 'SIGN_METHOD')

config.read('./secret.ini')
PIN=config.get('eid', 'PIN')
ID_CHAIN=config.get('eid', 'ID_CHAIN')
PART_BETWEEN_BEGIN_AND_END_CERTIFICATE_OF_PUBLIC_KEY_CERTIFICATE=config.get('eid', 'PART_BETWEEN_BEGIN_AND_END_CERTIFICATE_OF_PUBLIC_KEY_CERTIFICATE')

with open('./password.txt') as f:
    account_password = f.read()
with open('./salas_conf/miner_address.txt') as f:
    miner_address = f.read()

with open(f'{CONTRACT_PATH}/salas_contract.sol') as f:
    solidity_code = f.read()

# get web3.py instance, and unlock the default account
try:
    w3 = w3 = Web3(Web3.IPCProvider(IPC_PATH))
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

# calculate the signature of the address of the client/miner
# TODO: get from environment and check the stdout from the subprocess
print(f"signing miner address {miner_address} with private key ")
signing_process_1 = subprocess.run([f"cat", "./salas_conf/miner_address.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                                 , PART_BETWEEN_BEGIN_AND_END_CERTIFICATE_OF_PUBLIC_KEY_CERTIFICATE
                                 , signed_address).transact({
                                     'from': miner_address,
                                     'to': SALAS_CONTRACT_ADDRESS,
                                     'value': SALAS_CONTRACT_COST
                                 })
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Transaction receipt mined:")
pprint.pprint(dict(tx_receipt))
print("\nWas transaction successful?")
pprint.pprint(tx_receipt["status"])

with open("./salas_conf/miner_address_registered.txt", "w") as f:
    f.write("1")