#!/bin/bash

##-------------- Peer nodes given parameter -------------------------------------
CONTAINER_NAME=$1
NODE_NAME=$2

## Check container name
if [[ "" == $1 ]]; then
	CONTAINER_NAME="swarm-node"
	echo "Use default container name: $CONTAINER_NAME"
fi

## run add_peer.sh
swarm_cmd="/home/docker/swarm/cmd/add_peer.sh"
./docker_exec.sh $CONTAINER_NAME root "$swarm_cmd"