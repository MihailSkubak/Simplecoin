import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask import jsonify, request
from flask import Flask


class Blockchain:
    def __init__(self):
        self.c_transactions = []
        self.chain = []
        self.nodes = set()
        self.new_block(previous_hash='1', proof=100)

    def registration(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Nieprawidlowy URL')

    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'time_tamp': time(),
            'transactions': self.c_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.c_transactions = []

        self.chain.append(block)
        return block

    def proof_of_work(self, last_block):

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def transaction_creare(self, nadawca, odbiorca, ile):
        self.c_transactions.append({
            'nadawca': nadawca,
            'odbiorca': odbiorca,
            'ilosc': ile,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/transactions', methods=['POST'])
def transaction():
    values = request.get_json()
    required = ['nadawca', 'odbiorca', 'ilosc']
    if not all(k in values for k in required):
        return 'Brakujace wartosci', 400

    index = blockchain.transaction_creare(values['nadawca'], values['odbiorca'], values['ilosc'])
    response = {'Wiadomosc': f'Transakcja dodana do bloku {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():

    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    blockchain.transaction_creare(
        nadawca="0",
        odbiorca=node_identifier,
        ile=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200