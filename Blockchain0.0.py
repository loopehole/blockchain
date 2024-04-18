import datetime # use to get the current date time when the block is added to the blockchain
import hashlib # use for crypptographich purpose either sha256 or other, we will encode our data into hexadecimal code
import json
from flask import Flask, jsonify, request # to build web app using flask over the local host
import requests
from uuid import uuid4 #UUIDs are used to uniquely identify information without significant central coordination.
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions
        }
        self.chain.append(block)
        self.transactions = []
        return block
    
    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        isContinue = False
        while isContinue is False:
            hash_operation = hashlib.sha3_256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                isContinue = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_valid_chain(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            proof = block['proof']
            previous_proof = previous_block['proof']
            hash_operation = hashlib.sha3_256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            "Sender": sender,
            "Receiver": receiver,
            "Amount": amount
            }
        )

blockchain = Blockchain()
app = Flask(__name__)

@app.route('/mineBlock', methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': "Congratulations! You mined a block!",
        'index': block['index'],  # Fixed indexing issue here
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response)

@app.route('/getChain', methods=["GET"])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response)

@app.route('/isValidchain', methods=["GET"])
def is_valid_chain():
    if blockchain.is_valid_chain(blockchain.chain):
        response = {
            'message': "Congratulations! you have a valid chain",
            'length': len(blockchain.chain)
            }
    else:
        response = {
            'message': "The chain is not Valid"
        }
    return jsonify(response)
# Decentralising Blockchain0.0

if __name__ == "__main__":
    app.run(host='localhost', port=8000)