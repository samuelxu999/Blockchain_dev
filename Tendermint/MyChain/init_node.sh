#!/bin/bash

NODE_DIR='./node'


# Referenc: https://docs.tendermint.com/master/introduction/quick-start.html
#Initialize node, using 'tendermint init --help' to get more
tendermint init --home $NODE_DIR

# Show node ID
tendermint show_node_id --home $NODE_DIR
