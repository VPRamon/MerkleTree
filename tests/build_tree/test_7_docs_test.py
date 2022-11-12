import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.mtree import Mtree

from tests.test_utils import verify_hash
from tests.build_tree.test_4_docs_test import validate_4_docs_mtree

import pprint
from hashlib import sha256


# CONSTANTS
PREFIX_DOC  = 'DDDDD'
PREFIX_NODE = 'NNNNN'
NUM_OF_DOCS = 7

@pytest.fixture(autouse=True)
def setup_test(TEARDOWN_FIXTURE, request):

    test_helpers = TEARDOWN_FIXTURE['TestHelpers']
    test_helpers.setupDocs(NUM_OF_DOCS)
    yield {"TestHelpers" : test_helpers}


def validate_7_docs_mtree(docs, mtree):
    
    # Validate subtree (docs from 0 to 3)
    validate_4_docs_mtree(docs[:4], mtree)

    # Hash document 4
    HASH_DOC_4 = sha256( docs[4] ).hexdigest()
    assert mtree.tree[(0,4)].getHash() == HASH_DOC_4

    # Hash document 5
    HASH_DOC_5 = sha256( docs[5] ).hexdigest()
    assert mtree.tree[(0,5)].getHash() == HASH_DOC_5

    # Hash document 6
    HASH_DOC_6 = sha256( docs[6] ).hexdigest()
    assert mtree.tree[(0,6)].getHash() == HASH_DOC_6

    """ -- HASH LEVEL 1 --
    """
    HASH_NODE_1_2 = verify_hash(HASH_DOC_4, HASH_DOC_5, mtree.tree[(1,2)].getHash())

    HASH_NODE_1_3 = HASH_DOC_6
    assert mtree.tree[(1,3)].getHash() == HASH_NODE_1_3

    """ -- HASH LEVEL 2 --
    """
    HASH_NODE_2_1 = verify_hash(HASH_NODE_1_2, HASH_NODE_1_3, mtree.tree[(2,1)].getHash())

    """ -- HASH LEVEL 3 (root) --
    """
    HASH_NODE_3_0 = verify_hash(mtree.tree[(2,0)].getHash(), HASH_NODE_2_1, mtree.tree[(3,0)].getHash() )


def test_construct_6_docs_mtree(setup_test):

    mtree = Mtree()
    mtree.construct("documents")

    #''' Display Tree
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(mtree.tree)
    #mtree.draw()
    #'''

    """ -- HASH LEVEL 0 --
    """
    DOC_0 = bytes((PREFIX_DOC+'hello 0').encode('utf-8'))
    DOC_1 = bytes((PREFIX_DOC+'hello 1').encode('utf-8'))
    DOC_2 = bytes((PREFIX_DOC+'hello 2').encode('utf-8'))
    DOC_3 = bytes((PREFIX_DOC+'hello 3').encode('utf-8'))
    DOC_4 = bytes((PREFIX_DOC+'hello 4').encode('utf-8'))
    DOC_5 = bytes((PREFIX_DOC+'hello 5').encode('utf-8'))
    DOC_6 = bytes((PREFIX_DOC+'hello 6').encode('utf-8'))

    validate_7_docs_mtree([DOC_0,DOC_1,DOC_2,DOC_3,DOC_4,DOC_5,DOC_6], mtree)
