import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.mtree import Mtree
import pprint

from hashlib import sha256


# CONSTANTS
PREFIX_DOC  = 'DDDDD'
PREFIX_NODE = 'NNNNN'
NUM_OF_DOCS = 6

@pytest.fixture(autouse=True)
def setup_test(TEARDOWN_FIXTURE, request):

    test_helpers = TEARDOWN_FIXTURE['TestHelpers']
    test_helpers.setupDocs(NUM_OF_DOCS)
    yield {"TestHelpers" : test_helpers}


def test_construct_6_docs_mtree(setup_test):

    tree = Mtree()
    tree.construct("documents")

    #''' Display Tree
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tree.tree)
    tree.draw()
    #'''

    """ -- HASH LEVEL 0 --
    """
    DOC_0 = bytes((PREFIX_DOC+'hello 0').encode('utf-8'))
    DOC_1 = bytes((PREFIX_DOC+'hello 1').encode('utf-8'))
    DOC_2 = bytes((PREFIX_DOC+'hello 2').encode('utf-8'))
    DOC_3 = bytes((PREFIX_DOC+'hello 3').encode('utf-8'))
    DOC_4 = bytes((PREFIX_DOC+'hello 4').encode('utf-8'))
    DOC_5 = bytes((PREFIX_DOC+'hello 5').encode('utf-8'))

    # Hash document 0
    HASH_DOC_0 = sha256( DOC_0 ).hexdigest()
    assert tree.tree[(0,0)].getHash() == HASH_DOC_0

    # Hash document 1
    HASH_DOC_1 = sha256( DOC_1 ).hexdigest()
    assert tree.tree[(0,1)].getHash() == HASH_DOC_1

    # Hash document 2
    HASH_DOC_2 = sha256( DOC_2 ).hexdigest()
    assert tree.tree[(0,2)].getHash() == HASH_DOC_2

    # Hash document 3
    HASH_DOC_3 = sha256( DOC_3 ).hexdigest()
    assert tree.tree[(0,3)].getHash() == HASH_DOC_3

    # Hash document 4
    HASH_DOC_4 = sha256( DOC_4 ).hexdigest()
    assert tree.tree[(0,4)].getHash() == HASH_DOC_4

    # Hash document 5
    HASH_DOC_5 = sha256( DOC_5 ).hexdigest()
    assert tree.tree[(0,5)].getHash() == HASH_DOC_5

    """ -- HASH LEVEL 1 --
    """
    NODE_1_0 = bytes(( PREFIX_NODE + HASH_DOC_0 + HASH_DOC_1 ).encode('utf-8'))
    NODE_1_1 = bytes(( PREFIX_NODE + HASH_DOC_2 + HASH_DOC_3 ).encode('utf-8'))
    NODE_1_2 = bytes(( PREFIX_NODE + HASH_DOC_4 + HASH_DOC_5 ).encode('utf-8'))

    # Hash Node (1,0) which is concatenation of hashed doc0 & hashed doc1
    HASH_NODE_1_0 = sha256( NODE_1_0 ).hexdigest()
    assert tree.tree[(1,0)].getHash() == HASH_NODE_1_0

    # Hash Node (1,1) which is concatenation of hashed doc2 & hashed doc3
    HASH_NODE_1_1 = sha256( NODE_1_1 ).hexdigest()
    assert tree.tree[(1,1)].getHash() == HASH_NODE_1_1

    HASH_NODE_1_2 = sha256( NODE_1_2 ).hexdigest()
    # Since document 4 is an orphan child. Node (1,2) should be the same as Node (0,4)
    assert tree.tree[(1,2)].getHash() == HASH_NODE_1_2


    """ -- HASH LEVEL 2 --
    """
    NODE_2_0 = bytes(( PREFIX_NODE + HASH_NODE_1_0 + HASH_NODE_1_1 ).encode('utf-8'))
    NODE_2_1 = HASH_NODE_1_2

    # Hash Node (2,0) which is concatenation of hashed Node (1,0) & Node (1,1)
    HASH_NODE_2_0 = sha256( NODE_2_0 ).hexdigest()
    assert tree.tree[(2,0)].getHash() == HASH_NODE_2_0

    HASH_NODE_2_1 = NODE_2_1
    # Since Node (1,3) 4 is an orphan child. Node (2,1) should be the same as Node (1,2)
    assert tree.tree[(2,1)].getHash() == HASH_NODE_2_1


    """ -- HASH LEVEL 3 (root) --
    """
    NODE_3_0 = bytes(( PREFIX_NODE + HASH_NODE_2_0 + HASH_NODE_2_1 ).encode('utf-8'))

    # Hash Node (2,0) which is concatenation of hashed Node (1,0) & Node (1,1)
    HASH_NODE_3_0 = sha256( NODE_3_0 ).hexdigest()
    assert tree.tree[(3,0)].getHash() == HASH_NODE_3_0