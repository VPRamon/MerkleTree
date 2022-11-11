# Testing

This folder contains the set of test that verify the correct implementation of the MerkleTree and its functionalities.

### Run Test

Tests can be executed by means of `pytest` util.

```
pytest tests/
```

In order to debug a specific test, you can keep the artifcats generated at runtime by adding the flag `--keep_artifacts`

```
pytest tests/ -s --keep_artifacts -k `test-to-debug`
```