import json, time, os

import flask as fl
from web3 import Web3
from hexbytes import HexBytes

################
# CONSTANTS
################
COMPLETE_PATH_TO_MAP_FILE = './session/map_address_to_time.json'

################
# globals
################
faucet_start_server = os.getenv("FAUCET_START_SERVER")
app = fl.Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRETKEY")
FAUCET_SALAS_PER_DROP = float(os.getenv("FAUCET_SALAS_PER_DROP"))
FAUCET_TIMEOUT_IN_SECS = int(os.getenv("FAUCET_TIMEOUT_IN_SECS"))

# get w3 provider and secrets
IPC_PATH = '/salas/miner/geth.ipc'
w3 = Web3(Web3.IPCProvider(IPC_PATH))
with open('/salas/miner/secrets/password.txt') as f:
    account_password = f.read()
with open('/salas/miner/conf/node_address.txt') as f:
    miner_address = f.read()

# Dict to storage when an address received salas (address -> time) 
map_address_time = {}

################
# Flask app routes
################
@app.route("/")
def index():
    return fl.render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    address = None
    if "address" in fl.request.form:
        address = fl.request.form.get("address")
        if address == "":
            fl.flash('Address empty. Please fill in your public address')
            return fl.redirect(fl.url_for("index"))
    else:
        fl.flash('No address received. Please fill in your public address')
        return fl.redirect(fl.url_for("index"))
    
    timestamp = int(time.time())
    print(f"faucet balance is {w3.eth.get_balance(miner_address)}")

    if w3.eth.get_balance(miner_address) < 2 * FAUCET_SALAS_PER_DROP:
        fl.flash("The faucet is empty. Try again later.")
        return fl.redirect(fl.url_for("index"))

    if address not in map_address_time or (timestamp - map_address_time[address]) >= FAUCET_TIMEOUT_IN_SECS:
        print(f"sending salas to {address}")
        txn = sendSalas(address, FAUCET_SALAS_PER_DROP, miner_address)

        if txn != None:
            storeTxnInMap(address, timestamp)
            fl.flash(fl.Markup("Congrats. See you on the moon \n without having destroyed our planet in doing soo ;) "))
        else:
            fl.flash("An error was encountered. Please check your address and retry.")
    else:
        fl.flash(f"You have already receive SALAS today. You will be able to receive an new faucet drop in {FAUCET_TIMEOUT_IN_SECS - (timestamp - map_address_time[address])} seconds")
    return fl.redirect(fl.url_for("index"))

def storeTxnInMap(address: str, timestamp: int):
    map_address_time[address] = timestamp

    with open(COMPLETE_PATH_TO_MAP_FILE, "w") as f:
        json.dump(map_address_time, f, indent=4, sort_keys=True)

def sendSalas(address: str, amount: float, from_address: str):
    txn = None

    address = HexBytes(address)
    from_address = HexBytes(from_address)

    try:
        txn = w3.eth.send_transaction({
            'to': address,
            'from': w3.eth.coinbase,
            'value': w3.toWei(amount,'ether')
        })
    except Exception as e:
        print("Unable to send the transaction. " + str(e))

    return txn

def setup():
    global map_address_time

    # make a transactions DB if it does not yet exist
    if not os.path.exists(COMPLETE_PATH_TO_MAP_FILE):
        with open(COMPLETE_PATH_TO_MAP_FILE, 'a') as f:
            json.dump({}, f, indent=4, sort_keys=True)

    with open(COMPLETE_PATH_TO_MAP_FILE, "r") as f:
        map_address_time = json.load(f)

if __name__ == "__main__":
    if faucet_start_server == 'yes':
        setup()
        app.run(host="0.0.0.0", port=8080)
    else:
        print("Not launcing the faucet. Set the command in .env.cmd file if you need the faucet.")