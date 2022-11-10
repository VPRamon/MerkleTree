from hashlib import sha256
from mtree import Mtree
import pprint


tree = Mtree()

tree.construct("documents")

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tree.tree)

tree.draw()

# tree.modifyDocument("doc0.dat", "Bye 0")

# tree.draw()

# tree.modifyDocument("doc0.dat", "Hello 0")

# tree.createTxtFile()

print(tree.getPoM('doc4.dat', 4))