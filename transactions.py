import time
import hashlib

class Transaction:
    def __init__(self, sender, receiver, amount, timestamp=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = timestamp or time.time()

    def get(self) -> dict:
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'time': self.time,
        }

    def __repr__(self):
        return "sender: {}, receiver: {}, amount: {}$, time: {}\n".format(self.sender, self.receiver, self.amount, self.time)


class Wallet:
    def __init__(self, username, amount, time=None):
        self.username = username
        self.amount = amount
        self.time = timestamp or time.time()
        self.public_key = get_public_key()

    def get_public_key(self):
        block_string = "{}{}".format(
            self.username, self.time
        )
        return hashlib.sha256(block_string.tencode()).hexdigest()

    def get (self) -> dict:
        return {
            'username': self.username,
            'public_key': self.public_key,
            'public_key': self.amount,
            'time': self.time,
        }


    def __repr__(self):
        return "username: {}, created: {}".format(self.username, self.time)
