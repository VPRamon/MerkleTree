# Merkle Tree

This repository contains an implementation of Merkle Trees fully written in Python.

Implemented features
- Creating tree from directory of documents.
- Adding nodes to the tree.
- Modifying nodes of the tree.
- Proof of existence in the tree.
- Exporting tree in `.dat` format.
- Drawing tree in terminal.

> See `tests` folder to how to run the tests on the different features. 

## Example
An example of how to use the classes can be found in `example.py`.

1. Constructing tree from documents
```{python}
tree = Mtree()
tree.construct('documents')
```

2. Adding documents
```{python}
tree.addDocument('documents', 'hello 4')
```

3. Modifying documents
```{python}
tree.modifyDocument('doc4.dat', 'bye 4')
```

4. Generating PoM (generates file `pom5.dat`)
```{python}
tree.savePoM(5, 'pom5.dat')
```

5. Verifying PoM (returns bool)
```{python}
ver = tree.verifyPoM('doc5.dat', 5)
```

6. Export tree to text file
```{python}
tree.createTxtFile()
```

7. Visualizing tree in terminal (shows only first 4 hex letters of each hash)
```{python}
tree.draw()
```
The result:
```{bash}
|_ 8b73
    |_ 1d66
        |_ fbaf
            |_ f5cb
            |_ 7aa4
        |_ 722e
            |_ dd8e
            |_ 2c54
    |_ a9f8
        |_ a9f8
            |_ 1677
            |_ a069
```