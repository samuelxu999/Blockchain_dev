#!/bin/bash

## ============= Run cluster by launching multiple containerized swarm nodes given args ==============
OPERATION=$1

## Start cluster
if  [ "start" == "$OPERATION" ] ; then
	echo "Start 6 swarm nodes"
	./service_run.sh start swarm-node1 30401 8501 8581
	./service_run.sh start swarm-node2 30402 8502 8582
	./service_run.sh start swarm-node3 30403 8503 8583
	./service_run.sh start swarm-node4 30404 8504 8584
	./service_run.sh start swarm-node5 30405 8505 8585
	./service_run.sh start swarm-node6 30406 8506 8586

## Stop cluster
elif [ "stop" == "$OPERATION" ] ; then
	echo "Stop swarm nodes"
	./service_run.sh stop swarm-node1
	./service_run.sh stop swarm-node2
	./service_run.sh stop swarm-node3
	./service_run.sh stop swarm-node4
	./service_run.sh stop swarm-node5
	./service_run.sh stop swarm-node6

## Stop cluster
elif [ "peer" == "$OPERATION" ] ; then
	echo "Peer swarm nodes."
	./peer_node.sh swarm-node1
	./peer_node.sh swarm-node2
	./peer_node.sh swarm-node3
	./peer_node.sh swarm-node4
	./peer_node.sh swarm-node5
	./peer_node.sh swarm-node6

## show cluster
elif [ "show" == "$OPERATION" ] ; then
	echo "Show cluster"
	./service_run.sh show | grep swarm-node

## Show usage
else
	echo "Usage $0 -operation(start|stop|show)"
fi
