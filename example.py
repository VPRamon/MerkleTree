from src.mtree import Mtree
import os

####
# Create files for example
####

for i in range(4):
    f = open(f'documents/doc{i}.dat', 'w')
    f.write(f"hello {i}")
    f.close()

####
# Constructing tree from documents
####
print("Constructing tree from documents in ./documents/...")
tree = Mtree()
tree.construct('documents')

print("Drawing generated tree...")
tree.draw()
print("-"*30)

####
# Adding documents
####
print("Adding documents 4 and 5 to tree...")
tree.addDocument('documents', 'hello 4')
print("Drawing new tree...")
tree.draw()

tree.addDocument('documents', 'hello 5')

print("Drawing new tree...")
tree.draw()
print("-"*30)


####
# Modifying documents
####
print("Chainging content of document 4...")
tree.modifyDocument('doc4.dat', 'bye 4')

print("Drawing new tree...")
tree.draw()
print("-"*30)


####
# Proof of Membership
####
print("Proving that doc 5 exists in position 5")
ver1 = tree.verifyPoM('doc5.dat', 5)
print(f"PoM: {ver1} (see generated file pom.dat)")
tree.savePoM(5)

print("Proving that doc 5 does not exist in position 2")
ver2 = tree.verifyPoM('doc5.dat', 2)
print(f"PoM: {ver2}")

####
# Exporting to .dat file
####
print("Creating mtree.dat...")
tree.createTxtFile()
print("DONE! :)")


####
# Removing extra created files
####

for i in range(6):
    os.remove(f'documents/doc{i}.dat')