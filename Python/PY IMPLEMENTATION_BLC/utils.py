import hashlib

import redis


def encode(string, code='utf-8'):
    return string.encode(code)


def decode(string, code='utf-8'):
    return string.decode(code)


def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()


class DB(object):
    def __init__(self, host='localhost', port=6379, db=0, bucket='blocks'):
        self.bucket = bucket
        self.db = redis.Redis(host='localhost', port=6379, db=0)

    def put(self, key, val):
        self.db.hset(self.bucket, key, val)

    def get(self, key):
        return self.db.hget(self.bucket, key)
