# In this code we will be going to implement over multiple host
'''
Endpoints:
/mineBlock (GET): Mines a new block and adds it to the blockchain.
/getChain (GET): Returns the entire blockchain.
/isValidChain (GET): Checks if the blockchain is valid.
/addTransaction (POST): Adds a new transaction to the pending transactions list.
/connectNode (POST): Connects to a new node in the network.
/getNodes (GET): Returns the list of connected nodes.
'''
import datetime
import hashlib
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
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
        while not self.valid_proof(new_proof, previous_proof):
            new_proof += 1
        return new_proof

    def valid_proof(self, new_proof, previous_proof):
        guess = f'{new_proof**2 - previous_proof**2}'.encode()
        hash_operation = hashlib.sha256(guess).hexdigest()
        return hash_operation[:4] == '0000'

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
            if not self.valid_proof(block['proof'], previous_block['proof']):
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        if not all([sender, receiver, amount]):
            return False
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        return True

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/getChain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_valid_chain(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False


blockchain = Blockchain()
app = Flask(__name__)
CORS(app)
node_address = str(uuid4()).replace('-', '')  # Generate a unique node address


@app.route('/mineBlock', methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    blockchain.add_transaction(sender="0", receiver=node_address, amount=1)  # Reward for mining
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    response = {
        'message': "Congratulations! You mined a block!",
        'block': block
    }
    return jsonify(response), 200

@app.route('/getChain', methods=["GET"])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/isValidChain', methods=["GET"])
def is_valid_chain():
    is_valid = blockchain.is_valid_chain(blockchain.chain)
    response = {
        'message': "The chain is valid" if is_valid else "The chain is not valid"
    }
    return jsonify(response), 200

@app.route('/addTransaction', methods=["POST"])
def add_transaction():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No JSON data provided'}), 400

    sender = json_data.get('sender')
    receiver = json_data.get('receiver')
    amount = json_data.get('amount')

    if not all([sender, receiver, amount]):
        return jsonify({'message': 'Missing required fields'}), 400

    if blockchain.add_transaction(sender, receiver, amount):
        response = {'message': 'Transaction added successfully'}
        return jsonify(response), 201
    else:
        response = {'message': 'Failed to add transaction'}
        return jsonify(response), 500

@app.route('/connectNode', methods=["POST"])
def connect_node():
    json_data = request.get_json()
    nodes = json_data.get('nodes')
    if not nodes:
        response = {'message': 'No nodes provided'}
        return jsonify(response), 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'Nodes added successfully',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/getNodes', methods=["GET"])
def get_nodes():
    response = {
        'nodes': list(blockchain.nodes)
    }
    return jsonify(response), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
