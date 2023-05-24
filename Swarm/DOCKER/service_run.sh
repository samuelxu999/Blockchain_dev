#!/bin/bash


##-------------- Run constainer as background service given args -------------------------------------

OPERATION=$1
CONTAINER_NAME=$2
RPC_PORT=$3
BZZ_PORT=$4
PORT=$5

## Check container name
if [[ "" == $2 ]]; then
	CONTAINER_NAME="swarm-node"
	echo "Use default container name: $CONTAINER_NAME"
fi

## Start container
if  [ "start" == "$OPERATION" ]; then
	echo "Startup service!"

	if ! [[ $RPC_PORT =~ ^[0-9]+$ ]]; then
		echo "Error: rpcport should be integer!"
		exit 0
	fi

	if ! [[ $PORT =~ ^[0-9]+$ ]]; then
		echo "Error: port should be integer!"
		exit 0
	fi

	if ! [[ $BZZ_PORT =~ ^[0-9]+$ ]]; then
		echo "Error: bzz_port should be integer!"
		exit 0
	fi

	IMAGE_FILE="samuelxu999/swarm_node:x86"
	## prepare docker image
	docker pull "$IMAGE_FILE"
	docker tag "$IMAGE_FILE" swarm_node

	# IMAGE_FILE="swarm_node"

	# bootup container node
	./run_bash.sh $CONTAINER_NAME

	## run Swarm service app
	app_cmd="python3 Swarm_Server.py --threaded --port $PORT --bzz_port $BZZ_PORT"
	./docker_exec.sh $CONTAINER_NAME docker "$app_cmd" &>/dev/null &

	## run swarm node 
	swarm_cmd="/home/docker/swarm/cmd/run_node.sh $BZZ_PORT $RPC_PORT"
	./docker_exec.sh $CONTAINER_NAME root "$swarm_cmd" &>/dev/null &
	

## Stop container
elif [ "stop" == "$OPERATION" ]; then
	echo "Stop running service!"
	docker container stop $CONTAINER_NAME
## List container
elif [ "show" == "$OPERATION" ]; then
	echo "Show running service!"
	docker container ls
## show usage
else
	echo "Usage $0 -operation(start|stop|show) -container_name(swarm-node@id) -rpc_port(30399) -bzz_port(8500) -port(8580)"
fi
