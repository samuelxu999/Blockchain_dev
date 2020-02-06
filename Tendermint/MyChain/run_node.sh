#!/bin/bash

NODE_DIR='./node'


# Referenc: https://docs.tendermint.com/master/introduction/quick-start.html

#Run a simple in-process application node
# tendermint node --home $NODE_DIR --proxy_app=kvstore


# Peering nodes
ID0='87ab784fb6e8d448d03340aeb02ff0ee4b2996dc'
IP0='128.226.88.250'

ID1='515abc266fc331897c5993d3be3c2c549bcce54b'
IP1='128.226.77.157'

ID2='14583fee32f315bf6344a3394690586a060f1034'
IP2='128.226.78.128'

ID3='9ce231c713ea7f9b0e3a193c5dbf08be2f0f0b68'
IP3='128.226.88.155'

ID4='4db2fe714d7321bbd51fb56a1c4ec70ae1d8f3b2'
IP4='128.226.79.31'

PEERS="$ID0@$IP0:26656,$ID1@$IP1:26656,$ID2@$IP2:26656,$ID3@$IP3:26656,$ID4@$IP4:26656"

#Run Cluster of Nodes
tendermint node --home $NODE_DIR --proxy_app=kvstore --p2p.persistent_peers="$PEERS"

