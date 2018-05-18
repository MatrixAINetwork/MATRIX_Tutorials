import pickle

from block import Block
from utils import DB


class Blockchain(object):
    """ Blockchain keeps a sequence of Blocks

    Attributes:
        _tip (bytes): Point to the latest hash of block.
        _db (DB): DB instance
    """
    latest = 'l'

    def __init__(self):
        self._db = DB()
        self._tip = self._db.get('l')

        if not self._tip:
            block = Block().pow_of_block()
            self._db.put(block.hash, pickle.dumps(block))
            self._db.put(Blockchain.latest, block.hash)
            self._tip = block.hash

    def add_block(self, data):
        # AddBlock saves provided data as a block in the blockchain

        last_hash = self._db.get(Blockchain.latest)
        new_block = Block(data, last_hash)

        # Update DB with the new block
        self._db.put(new_block.hash, pickle.dumps(new_block))
        # Tip point to the new block
        self._db.put(Blockchain.latest, new_block.hash)
        # Update tip
        self._tip = new_block.hash

    @property
    def blocks(self):
        current_tip = self._tip
        while True:
            encoded_block = self._db.get(current_tip)
            block = pickle.load(encoded_block)
            yield block
            current_tip = block.prev_block_hash
