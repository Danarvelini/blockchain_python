from time import time
import json
from hashlib import sha3_256


class Blockchain(object):
    def __init__(self):
        self.blockchain = []
        self.current_transactions = []

        # Adding a initial block
        self.new_block(previous_hash=1, proof=200)

    @property
    def get_last_block(self):
        return self.blockchain[-1]

    @staticmethod
    def hash(block):
        encoded_json = json.dumps(block, sort_keys=True, indent=0)
        return sha3_256(sting=encoded_json).hexdigest()

    def new_block(self, proof, previous_hash=None):
        new_block = {
            "timestamp": time(),
            "index": len(self.blockchain) + 1,
            "last_hash": previous_hash,
            "proof": proof,
            "transactions": self.current_transactions,
        }

        self.current_transactions = []

        self.blockchain.append(new_block)
        return new_block

    def new_transaction(self, origin, destination, amount):
        self.current_transactions.append(
            {
                "origin": origin,
                "destination": destination,
                "amount": amount,
            }
        )

        return self.get_last_block["index"] + 1
