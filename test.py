# Import Flask and other required modules
import datetime
import hashlib
import json
from flask import Flask, jsonify, request, render_template  # Import render_template
from flask_cors import CORS
from uuid import uuid4
from urllib.parse import urlparse

# Create a Flask app instance
app = Flask(__name__)
CORS(app)

# Define the Blockchain class and other functionalities as before...
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

# Instantiate the Blockchain class
blockchain = Blockchain()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/mineBlock')
def mine_block():
    return render_template('mineBlock.html')

@app.route('/getChain')
def get_chain():
    return render_template('getChain.html')

@app.route('/isValidChain')
def is_valid_chain():
    return render_template('isValidChain.html')

@app.route('/addTransaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # Process the form submission
        sender = request.form.get('sender')
        receiver = request.form.get('receiver')
        amount = request.form.get('amount')
        # Perform the transaction processing logic
        return render_template('transactionSuccess.html')  # Render a success page
    else:
        return render_template('addTransaction.html')

@app.route('/connectNode', methods=['GET', 'POST'])
def connect_node():
    if request.method == 'POST':
        # Process the form submission
        node_url = request.form.get('node')
        # Perform the node connection logic
        return render_template('nodeConnected.html')  # Render a success page
    else:
        return render_template('connectNode.html')

@app.route('/getNodes')
def get_nodes():
    return render_template('getNodes.html')

# Run the Flask app
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
