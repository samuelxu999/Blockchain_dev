#!/bin/bash

# parse parameters
operation=$1
command_line=$2

## Start swarm_node containers
if  [ "start" == "$operation" ]; then
	echo "Start swarm_node!"
	command_line="cd $SWARMNODE;./service_run.sh start swarm-node 30399 8500 8580"
## Stop swarm_node containers
elif [ "stop" == "$operation" ]; then
	echo "Stop running swarm_node!"
	command_line="cd $SWARMNODE;./service_run.sh stop"
## Peer swarm_node containers
elif [ "peer" == "$operation" ]; then
	echo "Peer swarm_node!"
	command_line="cd $SWARMNODE;. ~/.profile;./peer_node.sh"
## Update swarm_node image
elif [ "update" == "$operation" ]; then
	echo "Update swarm_node image!"
	command_line="cd $SWARMNODE;git pull origin"
## execute remote test command
elif [ "test" == "$operation" ]; then
	echo "Execute remote test command!"
	if [ "$command_line" == "" ]; then
		# using default cmd.
		command_line="echo $SWARMNODE"
	fi
## show usage
else
	echo "Usage $0 -operation(start|stop|peer|update|test) -command_line(string)"
	exit 0
fi

# for iterate json to extract peering information
PEER_NODES='./swarm_cmd/static-nodes.json'
for k in $(jq  'keys | .[]' $PEER_NODES); do
	address=$(jq -r ".[$k].address" $PEER_NODES);
	ip=$(jq -r ".[$k].ip" $PEER_NODES);
	user=$(jq -r ".[$k].user" $PEER_NODES);

	# Use cut with : as the field delimiter and get desired fields f1:
	ip_address="$(cut -d ':' -f1 <<<"$ip")";
	ip_port="$(cut -d ':' -f2 <<<"$ip")";

	# skip localtest host
	if [ "$ip_address" != "0.0.0.0" ]; then
 		# echo "$user@$ip_address $command_line";
 		./ssh_remote_expect.sh $user $ip_address "$command_line"
	fi

done
