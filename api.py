from flask import Flask, request
from time import time
import json
import blockchain as bc

my_blockchain = bc.Blockchain()

app = Flask(__name__)

@app.route('/transactions/create', methods=['POST'])
def create_transaction():
    req_data = request.get_json()

    sender  = req_data['sender']
    recipient = req_data['recipient']
    amount = float(req_data['amount'])
    timestamp = int(time())
    privKey = req_data['privKey']
    my_blockchain.createTransaction(sender, recipient, amount, timestamp, privKey)
    print(my_blockchain.memPool)
    return ''

@app.route('/transactions/mempool', methods=['GET'])
def get_mempool():
    return { "mempool": my_blockchain.memPool }

@app.route('/mine', methods=['GET'])
def create_block():
    my_blockchain.createBlock()
    return ''

@app.route('/chain', methods=['GET'])
def show_chain():
    return json.dumps(my_blockchain.chain)

@app.route('/nodes/register', methods=['POST'])
def create_node():
    req_data = request.get_json()

    ip = req_data['ip']
    port = req_data['port']
    valid_address = ip+":"+port

    my_blockchain.nodes.add(valid_address)

    return valid_address

@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    

    return 