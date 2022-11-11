import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.mtree import Mtree
from tests.test_utils import verify_hash
import pprint

from hashlib import sha256


# CONSTANTS
PREFIX_DOC  = 'DDDDD'
PREFIX_NODE = 'NNNNN'
NUM_OF_DOCS = 4

@pytest.fixture(autouse=True)
def setup_test(TEARDOWN_FIXTURE, request):

    test_helpers = TEARDOWN_FIXTURE['TestHelpers']
    test_helpers.setupDocs(NUM_OF_DOCS)
    yield {"TestHelpers" : test_helpers}


def validate_4_docs_mtree(docs, mtree):

    assert len(docs) == NUM_OF_DOCS

    # Hash document 0
    HASH_DOC_0 = sha256( docs[0] ).hexdigest()
    assert mtree.tree[(0,0)].getHash() == HASH_DOC_0

    # Hash document 1
    HASH_DOC_1 = sha256( docs[1] ).hexdigest()
    assert mtree.tree[(0,1)].getHash() == HASH_DOC_1

    # Hash document 2
    HASH_DOC_2 = sha256( docs[2] ).hexdigest()
    assert mtree.tree[(0,2)].getHash() == HASH_DOC_2

    # Hash document 3
    HASH_DOC_3 = sha256( docs[3] ).hexdigest()
    assert mtree.tree[(0,3)].getHash() == HASH_DOC_3


    """ -- HASH LEVEL 1 --
    """
    # Hash Node (1,0) which is concatenation of hashed doc0 & hashed doc1
    HASH_NODE_1_0 = verify_hash(HASH_DOC_0, HASH_DOC_1, mtree.tree[(1,0)].getHash() )

    # Hash Node (1,1) which is concatenation of hashed doc2 & hashed doc3
    HASH_NODE_1_1 = verify_hash(HASH_DOC_2, HASH_DOC_3, mtree.tree[(1,1)].getHash() )

    """ -- HASH LEVEL 2 (root) --
    """
    HASH_NODE_2_0 = verify_hash(HASH_NODE_1_0, HASH_NODE_1_1, mtree.tree[(2,0)].getHash() )


def test_construct_4_docs_mtree(setup_test):

    mtree = Mtree()
    mtree.construct("documents")

    ''' Display Tree
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tree.tree)
    tree.draw()
    '''

    """ -- HASH LEVEL 0 --
    """
    DOC_0 = bytes((PREFIX_DOC+'hello 0').encode('utf-8'))
    DOC_1 = bytes((PREFIX_DOC+'hello 1').encode('utf-8'))
    DOC_2 = bytes((PREFIX_DOC+'hello 2').encode('utf-8'))
    DOC_3 = bytes((PREFIX_DOC+'hello 3').encode('utf-8'))

    validate_4_docs_mtree([DOC_0,DOC_1,DOC_2,DOC_3], mtree)