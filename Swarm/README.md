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
| add_peer.sh | This script is used to peer swarm nodes in static-nodes.json. |
| static-nodes.json | record all static peering enode information for private swarm test network. |

To run swarm node, you need to initialize a local node directory, like node1, and execute init_account.sh:

$ ./init_account.sh

After init_account.sh finished, a node1 wull be generated as well as an ethereum account in ./node1/keystore

If you have local node directory with an ethereum account, execute following scripts to run a swarm node:

$ ./run_node.sh node1 @account_address

The @account_addressn is ethereum account, like af53c65828ed52b370f6ecc5ccb6059cfba4b456.

$ ./add_peer.sh node1

Execute add_peer.sh will add peeriog nodes for current swarm instance. You need run this multiple if some nodes run with error in peering process.

	
## py_project
The Python development project including:

|   source   | Description |
|:----------:|-------------|
| RPC_Client.py | python RPC wrapper of curl commandlines for interacting with local swarm node |
| utilities.py | utils library to support projects. |

## Environment Setup	
The environement configuration includs: Prerequisite, Swarm development setup and Dapp development toolkit. Refer to env_setup.txt for detail.

--- env_setup.txt: The Swarm network and application development environment setup instruction.
