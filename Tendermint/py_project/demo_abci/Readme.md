# Demo ABCI application
Reference: https://github.com/davebryson/py-abci/tree/master/examples

1) The KVStoreApplication is a simple merkle key-value store. Transactions of the form key=value are stored as key-value pairs in the tree. Transactions without an = sign set both key and value to the value given. The app has no replay protection (other than what the mempool provides).

kvstore_go: https://github.com/tendermint/tendermint/tree/master/abci/example/kvstore

2) The counter app doesn't use a Merkle tree, it just counts how many times we've sent a transaction, asked for a hash, or committed the state. The result of commit is just the number of transactions sent.

counter_go: https://github.com/tendermint/tendermint/tree/master/abci/example/counter

# Install

```
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt --upgrade
python3 -m pip install eth_utils --upgrade
```

# RUN

Start the Python application on port `26658`

```
python3 kvstore.py
```

Start the tendermint node.

```
tendermint init
tendermint node
```

The application doesn't support  PersistentKVStoreApplication yet.
