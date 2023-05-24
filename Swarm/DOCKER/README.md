# swarm_node x86
This docker image built on Python3.6 includes: geth-1.7.3, go-1.13.7 and swarm-0.5.8.

The overview of contents of project are:

## Dockerfile
The Dockerfile defines all denpendencies, libs and app code inside the container.

## swarm_cmd

|   source   | Description |
|:----------:|-------------|
| add_peer.sh | This script is used to peer swarm nodes recorded in static-nodes.json.|
| run_node.sh | This script is used to start a swarm node given arguments: bzz_port and rpc_port. |
| static-nodes.json | record all static peering enode information for private swarm test network. |
| password.sec | password file for default account used by swarm node.|

## build.sh
$./build.sh make

The docker image 'swarm_node' will be built on your local environment.

Execute './build.sh clean' will remove built image. Similiar to using 'docker image rm -f @id'.

### To push image on docker hub docker hub.

1) Log in with your Docker ID

$docker login

2) Tag the image: 

$ docker tag imagename username/repository:tag

For example:

$ docker tag swarm_node samuelxu999/swarm_node:x86

3) Push the imagename by uploading your tagged image to the repository:

$ docker push username/repository:tag

For example:

$ docker push samuelxu999/swarm_node:x86

## run_bash.sh

$./run_bash.sh --container_name

For example, './run_bash.sh swarm-node'. After container startup, execue 'docker attach swarm-node (Replace with your container name)' to attach container with sh CLI.

To detach current container, pressing 'Ctrl+p' and 'Ctrl+q' to exit.

## docker_exec.sh

Run 'docker exec command' to interact with tools and scripts in container.

## service_run.sh

$./service_run.sh start --container_name --rpc_port --bzz_port --service port

Startup container and run services in container. For example, $./service_run.sh start swarm-node 30399 8500 8580

Execute './service_run.sh stop --container_name' can stop running container

Execute './service_run.sh show --container_name' can list all running container. Similiar to 'docker ps'.

## swarm_nodes.sh

Run './swarm_nodes.sh' to learn usage. This script can be used to manage swarm_node containers deployed on host machines.

## cluster_exec.sh

Run './cluster_exec.sh' to learn usage. This script can be used to start, show and stop 6 swarm nodes (containers) on the server. They can be used as a test demo swarm network.

## requirements.txt

this is used to install python packages in Dockerfile.



