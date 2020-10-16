# Swarm_dev
Implementation of the eth-Swarm enabled decentralized storage for IoT research

For Swarm documentation, please refer to: [Swarm Docs](https://swarm-guide.readthedocs.io/en/latest/index.html).

The overview of organization of project are:

## MySwarm
The private swarm network configuration folder, including:

|   source   | Description |
|:----------:|-------------|
| init_account.sh | node account initialization script to create eth account |
| run_node.sh | This script is used to a start swarm node with configuration. |
| add_peer.sh | This script is used to a start swarm node with configuration. |
| static-nodes.json | record all peers enode information for private network. |

	
## py_project
The Python development project including:

|   source   | Description |
|:----------:|-------------|
| RPC_Client.py | python RPC wrapper of curl commandlines for interacting with local swarm node |
| utilities.py | utils library to support projects. |

## Environment Setup	
The environement configuration includs: Prerequisite, Swarm development setup and Dapp development toolkit. Refer to env_setup.txt for detail.

--- env_setup.txt: The Swarm network and application development environment setup instruction.
