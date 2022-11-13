import os
import pytest

DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(DIR, '../documents')
NODES_DIR = os.path.join(DIR, '../nodes')

def pytest_addoption(parser):
    parser.addoption("--keep_artifacts", action="store_const", const=True)


class TestHelpers:

    @staticmethod
    def getDocs():
        documents = os.listdir(DOCS_DIR)
        # README.md file should not be considered a document
        documents.remove('README.md')
        return documents

    @staticmethod
    def getNodes():
        nodes = os.listdir(NODES_DIR)
        # README.md file should not be considered a node
        nodes.remove('README.md')
        return nodes

    @staticmethod
    def clearDocs():
        documents = TestHelpers.getDocs()
        for doc in documents:
            # print("removing: ",doc)
            doc_dir = os.path.join(DOCS_DIR, doc)
            os.remove(doc_dir)

    @staticmethod
    def clearNodes():
        nodes = TestHelpers.getNodes()
        for node in nodes:
            # print("removing: ",doc)
            doc_dir = os.path.join(NODES_DIR, node)
            os.remove(doc_dir)

    @staticmethod
    def createDoc(id, content):
        doc = os.path.join(DOCS_DIR, 'doc'+str(id)+'.dat')
        f = open(doc, "w")
        f.write(content)
        f.close()

    @staticmethod
    def setupDocs(n_docs):
        for id in range(n_docs):
            TestHelpers.createDoc(id, 'hello '+str(id))

@pytest.fixture()
def TEARDOWN_FIXTURE( request ):

    TestHelpers.clearDocs()
    TestHelpers.clearNodes()

    yield {"TestHelpers" : TestHelpers}

    if not request.config.getoption("--keep_artifacts"):
        TestHelpers.clearDocs()
        TestHelpers.clearNodes()
