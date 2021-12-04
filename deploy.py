import json
from web3 import Web3
from solcx import compile_standard, install_solc

import os
from dotenv import load_dotenv

load_dotenv()
# getting private_key from .env file (don't forget list .env in .gitignore!!!)
private_key = os.getenv("PRIVATE_KEY")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.6.0")

# Solidity source code (compile our contract)
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # 7545 for Ganache GUI
chain_id = 1337  # although my Ganache GUI shows Network ID 5777
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
# 0x added in front (if it's not there, e.g. from Ganache GUI) because python always look for hex format of private key
## never HARDCODE the private key like this ##

# run $ganache-cli --deterministic and keep it running in a separate shell
# --deterministic: so everytime we run Ganache, addresses and private keys won't change

# 1) build transaction
# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)
# {'value': 0, 'gas': 366119, 'chainId': 1337,...'to': b''}   'to' is blank because the contract deploys to the blockchain, instead a particular address

# 2) Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)

# 3) Send the signed transaction
print("Deploying Contract ... ")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# will see the transaction in Ganache GUI Transactions tab after $python3 deploy.py

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# 1) call
print(
    f"Initial Stored Value {simple_storage.functions.retrieve().call()}"
)  # which is 0

# 2) transact - need to go through the same 3-step of build/sign/send transactions as above
print("Updating stored Value...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,  # because there was a transaction above already
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
tx_store_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_store_hash)
print("Updated!")
print(simple_storage.functions.retrieve().call())  # will be 15 now
