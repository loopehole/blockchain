from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class Block:
    def __init__(self):
        self.transactions = []

class Wallet:
    def __init__(self):
        self.utxs = []

app = Flask(__name__)
block = Block()

t1 = Transaction("Juliet", "Alice", 0.95)
block.transactions.append(t1)

blockchain = Blockchain()
blockchain.chain.append(block)

@app.route('/mineBlock',methods=["GET"])
def mine_block():
    t = Transaction('Bob', 'Alice', 0.85)
    block.transactions.append(t)
    blockchain.chain.append(block)
    response = {
        "message":"Congratulations Block Mined Successfully"
    }
    return jsonify(response)

@app.route('/showBlockchain', methods=["GET"])  
def show_blockchain():  
    data = []
    for b in blockchain.chain:
        for t in b.transactions:
            transaction_data = {
                "Sender": t.sender,
                "Receiver": t.receiver,
                "Amount": t.amount
            }
            data.append(transaction_data)
    returnValues = {
        "Total Blocks": len(blockchain.chain),
        "Chain": data
    }
    return jsonify(returnValues)

if __name__ == "__main__":
    app.run(host='localhost', port=8080)
