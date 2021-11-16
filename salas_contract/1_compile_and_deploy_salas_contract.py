import sys, os

from web3 import Web3
from solcx import compile_source
import configparser

# need to do this if solc isn't found
#from solcx import install_solc
#install_solc(version='latest')

IPC_PATH = '../miner/geth.ipc'
with open('/salas/miner/secrets/password.txt') as f:
    password = f.read()
with open('./salas_contract.sol') as f:
    solidity_code = f.read()
with open('./conf/contract_deployed.txt') as f:
    contract_deployed = f.read()
with open('/salas/miner/conf/node_address.txt') as f:
    miner_address = f.read()

if os.getenv("CONTRACT_COMPILE_AND_DEPLOY") == 'no':
    print("Not compiling and deploying the contract code. This is probably what you want.")
    sys.exit(0)

if contract_deployed != '0':
    print("Salas contract already deployed.")
    sys.exit(0)

# get web3.py instance, and unlock the default account
try:
    w3 = w3 = Web3(Web3.IPCProvider(IPC_PATH))
    # set pre-funded account as sender
    _account = miner_address
    w3.eth.default_account = _account
    print(f"account; {_account}")
    print(f"password ; {password}")
    w3.geth.personal.unlock_account(_account, password, 600)
    print(f'current balance on default address ({_account}) is {w3.eth.get_balance(_account)}')
except FileNotFoundError as err:
    print("Can't connect to your IPC / server")
    raise err

# get the contract, bytecode and ABI
print("compiling source")
compiled_sol = compile_source(solidity_code)
contract_id, contract_interface = compiled_sol.popitem()
print("extracting bytecode and abi")
bytecode = contract_interface['bin']
abi = contract_interface['abi']

# deploy the contract and get the receipt
print("deploying bytecode of contract") 
Salas = w3.eth.contract(abi=abi, bytecode=bytecode)
print("making transaction")
tx_hash = Salas.constructor().transact()
print("waiting for transaction receipt")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print("received the transaction receipt ")
print(f'current balance on default address is {w3.eth.get_balance(_account)}')
print('**********************************')
print(f"the contract address is {contract_address}")
print('**********************************')

config = configparser.ConfigParser()
config.read('../conf/global/salas.ini')
config.set('main', 'SALAS_CONTRACT_ADDRESS', contract_address)

with open('../conf/global/salas.ini', 'w') as configfile:
    config.write(configfile)
