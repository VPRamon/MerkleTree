import src.utils.utils as utils

class Mnode():
    def __init__(self, _hash, parent=None, left=None, right=None):
        self.__hash = _hash
        self.__parent = parent
        self.__left = left
        self.__right = right

    @classmethod
    def fromChildNodes(cls, n1, n2, prefix=None):
        hash1 = n1.getHash()
        hash2 = n2.getHash()

        hash_val = utils.digest(hash1+hash2, prefix)
        n = cls(hash_val, parent=None, left=n1, right=n2)
        n1.setParent(n)
        n2.setParent(n)
        return n

    @classmethod
    def fromChildNode(cls, n1):
        hash_val = n1.getHash()
        n = cls(hash_val, parent=None, left=n1, right=None)
        n1.setParent(n)
        return n

    def setHash(self, _hash):
        self.__hash = _hash

    def getHash(self):
        return self.__hash

    def setParent(self, parent):
        self.__parent = parent

    def getParent(self):
        return self.__parent

    def getRightChild(self):
        return self.__right

    def setRightChild(self, right):
        self.__right = right

    def getLeftChild(self):
        return self.__left

    def setLeftChild(self, left):
        self.__left = left

    def recomputeHash(self, prefix):
        if self.getRightChild() is None:
            self.setHash(self.getLeftChild().getHash())
        else:    
            hash1 = self.getLeftChild().getHash()
            hash2 = self.getRightChild().getHash()

            hash_val = utils.digest(hash1+hash2, prefix)
            self.setHash(hash_val)

    
