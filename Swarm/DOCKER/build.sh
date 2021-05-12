#!/bin/bash

OPERATION=$1
IMAGE_NAME=$2


## Check image name
if [[ "" == $2 ]]; then
	IMAGE_NAME="swarm_node"
	#echo "Use default image $IMAGE_NAME ...!"
fi

## Liat all image
if [[ "list" == $OPERATION ]]; then
	echo "List image $IMAGE_NAME ...!"
	docker image ls $IMAGE_NAME
	#docker image ls

## Make image
elif [[ "make" == $OPERATION ]]; then
	echo "Start make $IMAGE_NAME ...!"

	## fetch go tar to local
	wget https://storage.googleapis.com/golang/go1.9.3.linux-amd64.tar.gz
	wget https://storage.googleapis.com/golang/go1.13.7.linux-amd64.tar.gz

	## new folders for local docker build
	if [ ! -d "app" ]
	then
		mkdir app
	fi
	## copy server and client code to localtest folder
	cp ../py_project/*.py app/

	docker build -t $IMAGE_NAME .

	## remove go tar
	rm go1.9.3.linux-amd64.tar.gz
	rm go1.13.7.linux-amd64.tar.gz

## Clean image given IMAGE_NAME
elif [[ "clean" == $OPERATION ]]; then
	echo "Remove $IMAGE_NAME ...!"
	docker image rm -f $IMAGE_NAME

else
	echo "Usage $0 cmd[list|make|clean|] image_name"
fi

