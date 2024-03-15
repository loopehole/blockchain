'''
- Here we will interact with smart contract with blockchain.
- We will be using functions to write transactions with smart contract.

'''
import json

from web3 import Web3

genache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(genache_url))

print(web3.is_connected())

#  this is to access the first default from ganche url for creating a transaction
web3.eth.default_account = web3.eth.accounts[0]

abi = json.loads("""[{"inputs":[],"name":"Greeter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"}]""")

# to_checksum_address is basically going to correctly format the address
address = web3.to_checksum_address(
    "0xd9145CCE52D386f254917e481eB44e9943F39138")

print(address)

# create a contract object
contract = web3.eth.contract(address=address, abi=abi)

print(contract)

# pritning greeting
# here call() will read the function from the contract
Greeting = contract.functions.greeting().transact() 
print(Greeting) 

# now we have to update the contract
# transact will create the transaction to the blockchain
tx_hash = contract.functions.setGreeting(
    "Hello from the other side").transact()
print(tx_hash)

# # now we have to wait for the transaction to be mined
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# print('Updated Greeting: {}'.format(contract.functions.greet().call()))
