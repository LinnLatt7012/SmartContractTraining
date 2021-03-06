from email.headerregistry import Address
from solcx import compile_standard, install_solc
import json
from web3 import Web3

import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            },
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

# get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/bd8832c4026945289f14ddb030334ecb")
)
chain_id = 4
my_address = "0xD354B0ec2372cAbc760a47eFe18805A52522c4EA"
private_key = os.getenv("PrivateKey")

# creating contact
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# geting latested transction
nonce = w3.eth.getTransactionCount(my_address)
# build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with contract
# Contract ABI
# Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Making Actual call
print("Before Transact")
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(10).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
# sign a transaction
store_signed_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# send a transaction
store_tx_hash = w3.eth.send_raw_transaction(store_signed_txn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print("After Transact")
print(simple_storage.functions.retrieve().call())
