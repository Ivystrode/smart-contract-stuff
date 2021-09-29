import json
import os

from solcx import compile_standard
from solcx import install_solc

from web3 import Web3
from dotenv import load_dotenv

load_dotenv() # looks for the .env file

install_solc("v0.6.0")

with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)
    
# compile the solidity

compiled_sol = compile_standard(
    {    
    "language": "Solidity",
    "sources": {"simpleStorage.sol":{"content": simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version = "0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
    
# get the bytecode iot deploy
bytecode = compiled_sol['contracts']['simpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['simpleStorage.sol']['SimpleStorage']['abi']

# how to deploy this on a simulated blockchain to test things easily
# GANACHE DOES THIS
# it creates a sim blockchain, so faster than using a testnet, and we can control the whole blockchain
# can use cli or gui appimage/ex file
# click quickstart to make a quick sim blockchain!
# see rpc server for url to connect to the blockchain

# ==========DEPLOY TO GANACHE==========
# use ganache to run a simulated blockchain locally
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x4D36Cdf19450C904F377EDc16ce20e559BF9939B"
# always need to add a 0x to a private key in python
private_key = os.getenv("GANACHE_PRIVATE_KEY")

# ==========DEPLOY TO A TESTNET OR MAINNET==========
# infura.io - gives you a url to connect to a blockchain
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/419f10d91878403ca1c12cd50177ec5b"))
chain_id = 3 # ROPSTEN
my_address = "0xF3900ca5C574254DaE270526EE85a53F3183af29"
private_key = os.getenv("ROPSTEN_PRIVATE_KEY")

# deploy to ganache, create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transcation to get the nonce
nonce = w3.eth.getTransactionCount(my_address) 
print("nonce:" + str(nonce)) # - will be 0 if the address hasn't been used before

# to deploy ths contract we need to make a transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId":chain_id,"from":my_address,"nonce":nonce})

# sign transaction iot deploy
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send this to the blockchain
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# interact and work with the contract
# need contract address and ABI
# so lets me a contract object to work with

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("Current FavNum value:")
print(simple_storage.functions.retrieve().call()) # we have to do .call() because we're not making a state change


# ==========CREATING A TRANSACTION==========
#to create a transaction (use the store function in simplestorage)
print("Updating contract...")
store_transaction = simple_storage.functions.store(76).buildTransaction({
    "chainId":chain_id,"from":my_address,"nonce":nonce + 1# because we already used the nonce when we used the initial transaction
})

# sign transaction
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

#send transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

#wait for tx to finish
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated")
print("New FavNum value:")
print(simple_storage.functions.retrieve().call()) # since we've now updated the "favourite number" that updated value is what we get back


