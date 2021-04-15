import time
import threading
import hashlib

from transactions import *

class Node:
    def __init__(self, parent, previous_hash, root_hash, difficulty_target, transactions, timestamp=None):
        # header
        self.parent = parent
        self.root_hash = root_hash
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.difficulty_target = difficulty_target
        # children
        self.left = None
        self.right = None

        # time and hash
        self.timestamp = timestamp or time.time()
        self.hash = self.get_block_hash()

    def get_block_hash(self):
        block_string = "{}{}{}".format(
            self.previous_hash, self.difficulty_target, self.timestamp
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_transactions(self, transactions: [Transaction]):
        self.transactions.extend(transactions)

    def __repr__(self):
        return "{}\t- {}\t- {}\nTransactions: [{}]".format(self.root_hash, self.previous_hash, self.difficulty_target, self.transactions)


class MerkleTree:
    def __init__(self, difficulty_target):
        self.nodes = []
        self.difficulty_target = difficulty_target
        self.root = self.create_node(Node(parent=None, previous_hash=None, root_hash=None, transactions=None,
                                          difficulty_target=difficulty_target))

    def create_node(self, transactions):
        # attach parent to new node
        n = len(self.nodes)
        parent_index = n//2
        if parent_index != 0:
            # if nodes are already in the blockchain
            parent_node = self.nodes[parent_index]
            node = Node(parent=parent_node, transactions=transactions,
                        root_hash=self.nodes[0].hash, previous_hash=parent_node.hash, difficulty_target=self.difficulty_target)
            self.nodes.append(node)
            # attach new node to parent
            if parent_index % 2 == 0:
                self.nodes[parent_index].left = node
            else:
                self.nodes[parent_index].right = node
        else:
            # create genesis block
            node = Node(parent=None, transactions=None, root_hash=None, previous_hash=None, difficulty_target=self.difficulty_target)
            self.nodes.append(node)


    def is_valid(self):
        l = len(self.nodes)
        for i in range(l//2, l):
            self.is_node_valid(i)
        return True

    def is_node_valid(self, position):

        if position <= 1:
            return

        parent_position = position//2
        left_child_hash = self.nodes[parent_position * 2].hash
        right_child_hash = '' if len(self.nodes) > (parent_position * 2 + 1) else self.nodes[parent_position * 2].hash
        pair_string = left_child_hash + right_child_hash
        hashed = hashlib.sha256(pair_string.encode()).hexdigest()

        if hashed != self.nodes[parent_position-1]:
            return False

        self.is_node_valid(parent_position)

        return True

    def __repr__(self):
        st = "root_hash\t previous_hash\t difficulty_target\n"
        for node in self.nodes:
            st += str(node) + "\n"
        return st
