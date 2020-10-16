# Swarm_dev
Implementation of the eth-Swarm enabled decentralized storage for IoT research

For Swarm documentation, please refer to: [Swarm Docs](https://swarm-guide.readthedocs.io/en/latest/index.html).

The overview of organization of project are:

## MySwarm
The private swarm network configuration folder, including:

|   source   | Description |
|:----------:|-------------|
| init_node.sh | node initialization script to initialize node folder |
| run_node.sh | This script is used to test netowork by using python ABCI app. |
| static-nodes.json | record all peers information for private tendermint network. |

	
## py_project
The Python development project including:

|   source   | Description |
|:----------:|-------------|
| RPC_Client.py | python RPC wrapper of curl commandlines for interacting with local swarm node |
| utilities.py | utils library to support projects. |

## Environment Setup	
The environement configuration includs: Prerequisite, Swarm development setup and Dapp development toolkit. Refer to env_setup.txt for detail.

--- env_setup.txt: The Swarm network and application development environment setup instruction.
