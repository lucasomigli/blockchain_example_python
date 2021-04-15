import time
import hashlib
import random

from merkle_tree import *


class Block (object):
    def __init__(self, position, previous_hash, timestamp=None):
        self.position = position
        self.index = random.random() * pow(10, 17)
        self.previous_hash = previous_hash
        self.merkleTree = MerkleTree(self.position)
        self.timestamp = timestamp or time.time()
        self.nonce = self.get_block_hash()

    def get_block_hash(self):
        block_string = "{}{}{}{}".format(
            self.index, self.previous_hash, self.merkleTree, self.timestamp
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(self.index, self.previous_hash, self.nonce, self.merkleTree, self.timestamp)


class BlockChain (object):

    # Initiation

    def __init__(self):
        self.chain: [Block] = []
        self.create_new_block()

    def create_new_block(self):
        previous_hash = 0
        if len(self.chain) != 0:
            previous_hash = self.chain[-1].get_block_hash()
        new_block = Block(position=len(self.chain),
                          previous_hash=previous_hash)
        self.chain.append(new_block)

        return new_block

    # Validation

    def is_valid(self):
        for i in range(len(self.chain)-1, 0, -1):
            if self.chain[i].previous_hash != self.chain[i-1].get_block_hash():
                return False
        return True

    def is_valid_block_at_position(self, pos):
        if pos > len(self.chain)-1 or pos < 1:
            return Exception("Not a valid block.")
        if self.chain[pos].previous_hash != self.chain[pos-1].get_block_hash():
            return False
        elif self.chain[pos].timestamp <= self.chain[pos-1].timestamp:
            return False

        return True

    def is_valid_block_at_id(self, _id):
        i = 0
        while _id != self.chain[i] and i < len(self.chain):
            i += 1
        return is_valid_block_at_position(i)

    # Printing

    def print_block_at_position(self, pos):
        print("index, previous_hash, nonce, merkleTree, timestamp")
        print(self.chain[i])

    def __repr__(self):
        out = "index, previous_hash, nonce, merkleTree,timestamp\n"
        for i in range(len(self.chain)-1, -1, -1):
            out +=  str(self.chain[i])
        return out