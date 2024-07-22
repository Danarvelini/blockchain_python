from hashlib import sha3_256
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import requests


class BlockchainNode:
    def __init__(self, node_id, chain=[]):
        self.node_id = node_id
        self.chain = chain
        self.pending_transactions = []
        self.nodes = set()

        self.new_block(proof=99, previous_hash=9999)

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode()

        return sha3_256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = sha3_256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block["previous_hash"] != self.hash_block(last_block):
                return False

            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f"http://{node}/chain", timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to node {node}: {e}")
                continue

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash_block(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, origin, destination, amount):
        self.pending_transactions.append({"origin": origin, "destination": destination, "amount": amount})


app = Flask(__name__)

node_id = str(uuid4()).replace("-", "")
blockchain_node = BlockchainNode(node_id)


@app.route("/chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain_node.chain, "length": len(blockchain_node.chain)}
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()

    if "origin" in values and "destination" in values and "amount" in values:
        blockchain_node.new_transaction(values["origin"], values["destination"], values["amount"])
        return jsonify({"message": "Transaction added to pending transactions"}), 201

    return jsonify({"error": "Invalid transaction data"}), 400


@app.route("/mine", methods=["GET"])
def mine():
    last_block = blockchain_node.chain[-1]
    last_proof = last_block["proof"]
    proof = blockchain_node.valid_proof(last_proof, 0)

    blockchain_node.new_transaction("0", node_id, 1)
    previous_hash = blockchain_node.hash_block(last_block)
    block = blockchain_node.new_block(proof, previous_hash)

    return jsonify({"message": "New block mined", "block": block}), 200


@app.route("/nodes/register", methods=["POST"])
def register_node():
    values = request.get_json()

    if "nodes" in values:
        for node in values["nodes"]:
            blockchain_node.register_node(node)

        return jsonify({"message": "Nodes registered"}), 201

    return jsonify({"error": "Invalid node data"}), 400


@app.route("/nodes/resolve", methods=["GET"])
def resolve_conflicts():
    replaced = blockchain_node.resolve_conflicts()

    if replaced:
        return jsonify({"message": "Chain was replaced", "new_chain": blockchain_node.chain}), 200

    return jsonify({"message": "Chain is ok", "chain": blockchain_node.chain}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
