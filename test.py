'''
Here we will be interaacting with the Ethereum blockchain.
'''
import json

from web3 import Web3

infura_url = "https://mainnet.infura.io/v3/b5a8c9b444f443aea8b39b9ac7baafe3"
web3 = Web3(Web3.HTTPProvider(infura_url))

print(web3.is_connected())

Latest = web3.eth.block_number
print(Latest)

block = web3.eth.get_block(Latest)
print(block)

for i in range(0, 5):
  print(web3.eth.get_block(Latest - 5))
hash = '0xc277560947c447223c68cf782a736e07dafafaf4be2777cbc8316c0b102f9217'

print(web3.eth.get_transaction_by_block(hash, 2))
