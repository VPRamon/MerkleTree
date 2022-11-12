import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.mtree import Mtree
from tests.test_utils import verify_hash
from tests.build_tree.test_5_docs_test import validate_5_docs_mtree
from tests.build_tree.test_6_docs_test import validate_6_docs_mtree

import pprint
from hashlib import sha256


# CONSTANTS
PREFIX_DOC  = 'DDDDD'
PREFIX_NODE = 'NNNNN'
NUM_OF_DOCS = 5

@pytest.fixture(autouse=True)
def setup_test(TEARDOWN_FIXTURE, request):

    test_helpers = TEARDOWN_FIXTURE['TestHelpers']
    test_helpers.setupDocs(NUM_OF_DOCS)
    yield {"TestHelpers" : test_helpers}


def test_add_6th_doc(setup_test):

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
    DOC_4 = bytes((PREFIX_DOC+'hello 4').encode('utf-8'))
    NEW_DOC_5 = bytes((PREFIX_DOC+'hello 5').encode('utf-8'))

    docs = [DOC_0,DOC_1,DOC_2,DOC_3,DOC_4,NEW_DOC_5]

    # Validate subtree (docs from 0 to 5)
    validate_5_docs_mtree(docs[:5], mtree)

    # Create new doc
    mtree.addDocument("",'hello 5')

    # Validate subtree (docs from 0 to 3)
    validate_6_docs_mtree(docs, mtree)

    ''' Display Tree
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(mtree.tree)
    mtree.draw()
    '''