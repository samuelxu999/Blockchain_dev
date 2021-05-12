#!/bin/bash

##---------------- Used for constainer startup and run background---------------------------------------
# -d 				run container in background and print container ID
# -i 				sets up an interactive session; -t allocates a pseudo tty; 
# --rm 				makes this container ephemeral
# -v /etc/localtime:/etc/localtime:ro 	make sure docker's time syncs with that of the host
# -v @volume:@docker_path				use volume mapping to docker folder to save swarm data
# -v @local_path:@docker_path			use local folder mapping to docker folder for cmd and configure
# --name=@container_name specify the name of the container; the image you want to run the container from swarm_node;
# using /bin/bash as default CMD

IMAGE_NAME="swarm_node"

CONTAINER_NAME=$1

## Check container name
if [[ "" == $1 ]]; then
	CONTAINER_NAME="swarm-node"
	echo "Use default container name: $CONTAINER_NAME"
fi

# execute docker run command
docker run -d -it --rm --network=host \
	--privileged=true \
	-v /etc/localtime:/etc/localtime:ro \
	-v $CONTAINER_NAME:/home/docker/swarm/node \
	-v $(pwd)/swarm_cmd:/home/docker/swarm/cmd \
	--name=$CONTAINER_NAME $IMAGE_NAME /bin/bash
