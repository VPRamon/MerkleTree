from hashlib import sha256

# CONSTANTS
PREFIX_DOC  = 'DDDDD'
PREFIX_NODE = 'NNNNN'

def verify_hash(hash1, hash2, expected_hash, prefix=None):
    if(prefix == None): prefix = PREFIX_NODE
    n = bytes(( prefix + hash1 + hash2 ).encode('utf-8'))
    hash_ = sha256( n ).hexdigest()
    assert hash_ == expected_hash
    return hash_