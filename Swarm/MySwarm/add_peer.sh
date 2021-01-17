#!/bin/bash

## export geth path to support remote script execution
export GOETHEREUM=~/Desktop/Github/Blockchain_dev/dev_sdk/go-ethereum/build
export PATH=$PATH:$GOETHEREUM/bin

# parse parameters
Node_Dir=$1

# for iterate json to extract peering information
PEER_NODES='static-nodes.json'
for k in $(jq  'keys | .[]' $PEER_NODES); do
	name=$(jq -r ".[$k].name" $PEER_NODES);
	ip=$(jq -r ".[$k].ip" $PEER_NODES);
	enode=$(jq -r ".[$k].enode" $PEER_NODES);

	#echo $name $ip $enode

	echo "AddPeer: $enode" 

	geth --exec="admin.addPeer('$enode')" attach "./$Node_Dir/bzzd.ipc"

done
