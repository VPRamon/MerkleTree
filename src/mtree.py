import src.utils.utils as utils
from src.mnode import Mnode

class Mtree():
    def __init__(self):
        self.tree = {}
        self.doc2node = {}
        self.doc_prefix = utils.readFile("src/utils/doc.pre")
        self.node_prefix = utils.readFile("src/utils/node.pre")
        self.root = None

        self.num_leaves = 0
        self.num_lvls = 0

    def construct(self, path):
        """
        Construct the tree from a list of documents
        @param self: The object pointer
        @param path: path to the list of documents
        """
        # Get leaf nodes
        for idx, doc in enumerate(utils.getAllDocuments(path)):
            node_name = (0, idx)
            hash_ = utils.digestDoc(doc, prefix=self.doc_prefix)
            self.tree[node_name] = Mnode(hash_)
            self.doc2node[doc] = self.tree[node_name]

        # Build tree bottom-up
        n = self.num_leaves = len(self.tree)
        lvl = 1
        while n > 1:
            for i in range(0, n//2):
                n1 = self.tree[(lvl-1, 2*i  )]
                n2 = self.tree[(lvl-1, 2*i+1)]

                self.tree[(lvl, i)] = Mnode.fromChildNodes(n1, n2, self.node_prefix)
                
                #n1.setParent(self.tree[(lvl, i)])
                #n2.setParent(self.tree[(lvl, i)])

            if n % 2 != 0:
                
                n1 = self.tree[(lvl-1, n-1)]

                self.tree[(lvl, n//2)] = Mnode.fromChildNode(n1)

                #n1.setParent(self.tree[node_name])

            n = (n//2) + (0 if n%2==0 else 1)
            lvl += 1
            
        self.num_lvls = lvl
        self.root = self.tree[(lvl-1, 0)]

    def addDocument(self, path, content):
        id_ = self.num_leaves
        docName = 'doc'+str(id_)+'.dat'
        f = open(f"documents/{docName}", "w")
        f.write(content)
        f.close()

        # TODO: add document in tree
        hash_ = utils.digest(content, self.doc_prefix)
        node = Mnode(hash_)
        self.tree[(0, self.num_leaves)] = node

        depth = utils.getDepth(self.num_leaves)
        n_nodes = self.num_leaves
        lvl = 0

        while( lvl <= depth ):

            if(n_nodes % 2):
                sibling = self.tree[(lvl, n_nodes-1)]
                parent = sibling.getParent()
                if(parent):
                    parent.setRightChild(node)
                    parent.recomputeHash(self.node_prefix)
                else:
                    parent = Mnode.fromChildNodes(sibling, node, self.node_prefix)
                    sibling.setParent(parent)
                    self.tree[(lvl+1, 0)] = parent
                    self.root = parent

                lvl += 1
                n_nodes //= 2

            else:
                parent = Mnode.fromChildNode(node)
                node.setParent(parent)
                lvl += 1
                n_nodes //= 2
                self.tree[(lvl, n_nodes)] = parent
                

            node = parent

        self.num_leaves += 1


    def modifyDocument(self, doc, new_content):
        f = open(f"documents/{doc}", "w")
        f.write(new_content)
        f.close()

        node = self.doc2node[doc]

        # Recompute document hash
        hash_val = utils.digestDoc(f"documents/{doc}", prefix=self.doc_prefix)
        node.setHash(hash_val)

        node = node.getParent()
        while node != self.root:
            node.recomputeHash(self.node_prefix)
            node = node.getParent()
        self.root.recomputeHash(self.node_prefix)

    
    def getPoM(self, doc, doc_pos):
        """Proof of Membership"""
        prev_node = self.doc2node[doc]
        node = self.doc2node[doc].getParent()
        lvl = 0
        pos = doc_pos
        res = []
        while node is not None:
            #print(lvl, pos)
            left = node.getLeftChild()
            right = node.getRightChild()

            hash_pos = (pos-1) if (pos % 2) else (pos+1)
            if left == prev_node and right is not None:
                res.append((lvl, hash_pos, right.getHash()))
            elif right == prev_node:
                res.append((lvl, hash_pos, left.getHash()))

            prev_node = node
            node = node.getParent()
            print(prev_node, node)
            lvl += 1
            pos = pos//2
        
        res.append((self.num_lvls-1, 0, self.root.getHash()))

        return res


    """
    REPRESENTATIONS
    """

    def createTxtFile(self, filename="mtree.dat"):
        f = open(filename, 'w')

        # Write header
        npre = utils.str2hex(self.node_prefix)
        dpre = utils.str2hex(self.doc_prefix)
        head = f"MerkleTree:sha1:{npre}:{dpre}:{self.num_leaves}:{self.num_lvls}:{self.root.getHash()}\n"
        lines = []
        for (lvl, idx), node in self.tree.items():
            lines.append(f"{lvl}:{idx}:{node.getHash()}\n")
        lines = [head] + lines
        
        f.writelines(lines)

        f.close()


    def draw_branch(self, node, tabs):
        if node is None:
            return
        print(" "*tabs, "|_ ", node.getHash()[0:4], sep="")
        self.draw_branch(node.getLeftChild(), tabs+4)
        self.draw_branch(node.getRightChild(), tabs+4)


    def draw(self):
        self.draw_branch(self.root, 0)
