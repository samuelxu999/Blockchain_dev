#!/bin/bash

# execute docker exec to run command and scripts on running docker

CONTAINER_NAME=$1
EXEC_USER=$2
CMD_LINE=$3


# arguments validation
if [[ 3 -ne $# ]]; then
	echo "Usage $0 container_name exec_user command_line"
	exit 0
fi

# check container
if  [ "" == "$CONTAINER_NAME" ] ; then
	echo "No container_name!"
	exit 0
fi

# check user
if  [ "" == "$EXEC_USER" ] ; then
	echo "Not valid exec_user!"
	exit 0
fi

# execute docker run command
docker exec -u $EXEC_USER $CONTAINER_NAME $CMD_LINE