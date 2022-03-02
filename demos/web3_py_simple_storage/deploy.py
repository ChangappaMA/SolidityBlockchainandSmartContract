from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

#Compile Solidity
install_solc("0.6.0")
complied_sol = compile_standard({
    "language" : "Solidity",
    "sources" : {"SimpleStorage.sol" : {"content": simple_storage_file}},
    "settings": {
        "outputSelection" : {
            "*" : {
                "*": ["abi", "metadata", "evm.bytecode","evm.sourceMap"]
            }
        }
    }
},
solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(complied_sol, file)

# get bytecode
bytecode = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abicode = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

#Create contract in python
SimpleStorage = w3.eth.contract(abi=abicode, bytecode=bytecode)
#get latest transaction
nonce = w3.eth.get_transaction_count(my_address)
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#Send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#working with the contract
# Contract Address
#Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abicode)

#Interacting with blockchain
#Call -> Simulate making the call and getting a return value
#Tranct -> Actually make a state change

#Initial Value of stored functions
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
})
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)

print(simple_storage.functions.retrieve().call())