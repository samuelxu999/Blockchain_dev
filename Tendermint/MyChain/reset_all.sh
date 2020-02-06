#!/bin/bash

NODE_DIR='./node'


# (unsafe) Remove all the data and WAL, reset this node's validator to genesis state
tendermint unsafe_reset_all --home $NODE_DIR

# (unsafe) Reset this node's validator to genesis state
# tendermint  unsafe_reset_priv_validator --home $NODE_DIR