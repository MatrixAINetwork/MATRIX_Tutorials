import time
import hashlib

import utils
from pow import Pow


class Block(object):
    """ Represents a new Block object.

    Args:
        data (string): Data to be sent.
        prev_block_hash (string): Hash of the previous Block. 

    Attributes:
        _timestamp (bytes): Creation timestamp of Block.
        _data (bytes): Data to be sent.
        _prev_block_hash (bytes): Hash of the previous Block.
        _hash (bytes): Hash of the current Block.
        _nonce (int): A 32 bit arbitrary random number that is typically used once.
    """

    def __init__(self, data='Genesis Block', prev_block_hash=''):
        self._timestamp = utils.encode(str(int(time.time())))
        self._data = utils.encode(data)
        self._prev_block_hash = utils.encode(prev_block_hash)
        self._hash = None
        self._nonce = None

    def pow_of_block(self):
        # Makes the proof of work of the current Block
        pow = Pow(self)
        nonce, hash = pow.run()
        self._nonce, self._hash = nonce, utils.encode(hash)
        return self

    @property
    def hash(self):
        return utils.decode(self._hash)

    @property
    def data(self):
        return utils.decode(self._data)

    @property
    def prev_block_hash(self):
        return utils.decode(self._prev_block_hash)

    @property
    def timestamp(self):
        return str(self._timestamp)

    @property
    def nonce(self):
        return str(self._nonce)
