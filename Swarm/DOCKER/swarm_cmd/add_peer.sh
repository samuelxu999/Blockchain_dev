#!/bin/bash

# parse parameters
Node_Dir="/home/docker/swarm/node"
geth_bin="/opt/go_proj/src/github.com/ethereum/go-ethereum/build/bin"

# for iterate json to extract peering information
PEER_NODES='/home/docker/swarm/cmd/static-nodes.json'
for k in $(jq  'keys | .[]' $PEER_NODES); do
	name=$(jq -r ".[$k].name" $PEER_NODES);
	ip=$(jq -r ".[$k].ip" $PEER_NODES);
	enode=$(jq -r ".[$k].enode" $PEER_NODES);

	#echo $name $ip $enode

	/bin/echo "AddPeer: $enode" 

	$geth_bin/geth --exec="admin.addPeer('$enode')" attach "$Node_Dir/bzzd.ipc"

done
