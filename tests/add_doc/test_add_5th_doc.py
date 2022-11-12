import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.mtree import Mtree
from tests.test_utils import verify_hash
from tests.build_tree.test_4_docs_test import validate_4_docs_mtree
from tests.build_tree.test_5_docs_test import validate_5_docs_mtree

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


def test_add_5th_doc(setup_test):

    mtree = Mtree()
    mtree.construct("documents")

    ''' Display Tree
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(mtree.tree)
    mtree.draw()
    '''

    """ -- HASH LEVEL 0 --
    """
    DOC_0 = bytes((PREFIX_DOC+'hello 0').encode('utf-8'))
    DOC_1 = bytes((PREFIX_DOC+'hello 1').encode('utf-8'))
    DOC_2 = bytes((PREFIX_DOC+'hello 2').encode('utf-8'))
    DOC_3 = bytes((PREFIX_DOC+'hello 3').encode('utf-8'))
    NEW_DOC_4 = bytes((PREFIX_DOC+'hello 4').encode('utf-8'))

    docs = [DOC_0,DOC_1,DOC_2,DOC_3,NEW_DOC_4]

    # Validate subtree (docs from 0 to 3)
    validate_4_docs_mtree(docs[:4], mtree)

    # Create new doc
    mtree.addDocument("",'hello 4')

    # Validate subtree (docs from 0 to 3)
    validate_5_docs_mtree(docs, mtree)

    ''' Display Tree
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(mtree.tree)
    mtree.draw()
    '''