import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from src.mtree import Mtree

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
    mtree = Mtree()
    mtree.construct("documents")
    yield {
            "TestHelpers" : test_helpers,
            "mtree" : mtree 
    }


def test_pom_doc_1_of_4(setup_test):

    mtree = setup_test["mtree"]
    pom = mtree.getPoM(0)

    EXPECTED_POM = [
        (0, 1, mtree.tree[(0,1)].getHash()),
        (1, 1, mtree.tree[(1,1)].getHash()),
        (2, 0, mtree.tree[(2,0)].getHash())
    ]

    assert pom == EXPECTED_POM
    assert mtree.verifyPoM('doc0.dat', 0, pom)
    assert mtree.verifyPoM('doc0.dat', 0)

def test_pom_doc_2_of_4(setup_test):

    mtree = setup_test["mtree"]
    pom = mtree.getPoM(1)

    EXPECTED_POM = [
        (0, 0, mtree.tree[(0,0)].getHash()),
        (1, 1, mtree.tree[(1,1)].getHash()),
        (2, 0, mtree.tree[(2,0)].getHash())
    ]

    assert pom == EXPECTED_POM
    assert mtree.verifyPoM('doc1.dat', 1, pom)
    assert mtree.verifyPoM('doc1.dat', 1)

def test_pom_doc_3_of_4(setup_test):

    mtree = setup_test["mtree"]
    pom = mtree.getPoM(2)

    EXPECTED_POM = [
        (0, 3, mtree.tree[(0,3)].getHash()),
        (1, 0, mtree.tree[(1,0)].getHash()),
        (2, 0, mtree.tree[(2,0)].getHash())
    ]

    assert pom == EXPECTED_POM
    assert mtree.verifyPoM('doc2.dat', 2, pom)
    assert mtree.verifyPoM('doc2.dat', 2)

def test_pom_doc_4_of_4(setup_test):

    mtree = setup_test["mtree"]
    pom = mtree.getPoM(3)

    EXPECTED_POM = [
        (0, 2, mtree.tree[(0,2)].getHash()),
        (1, 0, mtree.tree[(1,0)].getHash()),
        (2, 0, mtree.tree[(2,0)].getHash())
    ]

    assert pom == EXPECTED_POM
    assert mtree.verifyPoM('doc3.dat', 3, pom)
    assert mtree.verifyPoM('doc3.dat', 3)
