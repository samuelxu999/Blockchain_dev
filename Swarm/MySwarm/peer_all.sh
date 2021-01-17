#!/bin/bash

# parse parameters
command_line=$1

if [ "$command_line" == "" ]; then
	command_line="hostname"
fi

# for iterate json to extract peering information
PEER_NODES='static-nodes.json'
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
