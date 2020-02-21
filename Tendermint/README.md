# Tendermint_dev
Official implementation of the Tendermint Enabled Decentralized Security for IoT

For Tendermint project, please refer to: [Tendermint](https://github.com/tendermint/tendermint) on github.

The overview of organization of project are:

## MyChains
The private tendermint network configuration folder, including:

|   source   | Description |
|:----------:|-------------|
| genesis.json | genesis data for private blockchain network initialization. |
| init_node.sh | node initialization script to initialize node folder |
| reset_all.sh | reset all data and confiuration under --home folder |
| static-nodes.json | record all peers information for private tendermint network. |
| kvstore_run.sh | This script is used to test netowork by using kvstore or counter demo ABCI app. |
| run_node.sh | This script is used to test netowork by using python ABCI app. |
	
## py_project
The Python ABCI development project including:

|   source   | Description |
|:----------:|-------------|
| RPC_Client.py | python wrapper of curl abci for interacting with tendermint network through RPC |
| utilities.py | utils library to support projects. |
| demo_abci | using python to rewrite kvstore or counter demo ABCI apps. |

## Environment Setup	
The environement configuration includs: Prerequisite, Tendermint Blockchain setup and ABCI Development toolkit. Refer to env_setup.txt for detail.

--- env_setup.txt: The blockchain network and application development environment setup instruction.
