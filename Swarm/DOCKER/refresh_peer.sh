#!/bin/bash

# parse parameters
refresh_rate=$1

if [ "$refresh_rate" == "" ]; then
	# using default interval 60s.
	refresh_rate=600
fi

while true; 
do 
	# ./swarm_nodes.sh peer;
	./cluster_exec.sh peer

	echo "Wait $refresh_rate seconds for refreshing peers."
	sleep $refresh_rate; 
done
