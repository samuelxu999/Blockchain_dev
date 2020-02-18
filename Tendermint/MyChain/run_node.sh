#!/bin/bash

NODE_DIR='./node'
ABCI_DIR='../py_project/demo_abci'
ABCI_APP=$1
PEER_NODES='static-nodes.json'

# Referenc: https://docs.tendermint.com/master/introduction/quick-start.html

#Run a simple in-process application node
# tendermint node --home $NODE_DIR --proxy_app=kvstore


# for iterate json to extract peering information
PORT="26656"
for k in $(jq  'keys | .[]' $PEER_NODES); do
	address=$(jq -r ".[$k].address" $PEER_NODES);
	ip=$(jq -r ".[$k].ip" $PEER_NODES);
	# echo $address $ip
	PEER=$address'@'$ip':'$PORT
	let "i=i+1"
	if [ $i == 1 ]; then
		PEERS=$PEER
	else
		PEERS=$PEERS','$PEER
	fi
	# echo $PEER
done


if  [ "" == "$ABCI_APP" ] ; then
	# Run default kvstore demo abci application
	python3 $ABCI_DIR'/counter.py' &

	#Run Cluster of Nodes
	tendermint node --home $NODE_DIR --p2p.persistent_peers="$PEERS"	

else
	# Run abci application given by parameter
	python3 $ABCI_DIR'/'$ABCI_APP &

	#Run Cluster of Nodes
	tendermint node --home $NODE_DIR --p2p.persistent_peers="$PEERS"
fi