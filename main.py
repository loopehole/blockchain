'''
This program is to send 1 ether from account 1 to account 2.
'''

from web3 import Web3

genache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(genache_url))

print(web3.is_connected())

account_1 = "0xFd6d155557aDDcd6D365152Ed552028D1b246458"
account_2 = "0xe50B2eb803603516C1c01460d5C4179BAaF8636f"

private_key = "0x8ad8634923071c7d12281e47bcdd12fcf28e2f2bc563eafc1592480e45abb2d1"

# get the nonce
nonce = web3.eth.get_transaction_count(account_1)
# now lets build a transaction
tx = {
    'nonce': nonce,
    'to': account_2,
    'value': web3.to_wei('1', 'ether'),
    'gas': 21000,
    'gasPrice': web3.to_wei('40', 'gwei')
}

#  now we have to signed the trasaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(web3.to_hex(tx_hash))
