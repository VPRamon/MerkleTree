from hashlib import sha256
import os
import binascii

def digest(x, prefix=None):
    """
    Get the hex string of the sha256 hash digest of the input x
    """
    x = str(x).encode('utf-8')
    hash = sha256()
    if prefix is not None:
        prefix = prefix.encode('utf-8')
        hash.update(bytes(prefix+x))
    else:
        hash.update(bytes(x))
    return hash.hexdigest()

def readFile(src):
    """
    Read the content of a document
    """
    with open(src) as file:
        content = file.read()
    return content

def digestDoc(src, prefix=None):
    """
    Get the hex string of the sha256 digest of the document at src
    """
    content = readFile(src)
    if prefix is not None:
        return digest(prefix+content)

    return digest(content)

def getAllDocuments(dir):
    """
    Return all documents in the folder dir
    """
    doc_names = os.listdir(dir)
    doc_names.sort()
    for doc in doc_names:
        # check if current path is a file
        full_path = os.path.join(dir, doc)
        if os.path.isfile(full_path) and doc[-4:] == '.dat':
            yield full_path

def concatDocuments(src1, src2):
    """
    Return the concatenation of the content of two documents
    """
    content1 = readFile(src1)
    content2 = readFile(src2)

    return content1 + content2

def str2hex(s):
    s = s.encode('utf-8')
    return binascii.hexlify(bytes(s)).decode('utf-8')