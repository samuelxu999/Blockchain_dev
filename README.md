# Blockchain_dev
Official implementation of the BlendCAC-A Smart Contact Enabled Decentralized Capability-based Access Control Mechanism for IoT

The concept proof system is deployed on a private Ethereum network. For Ethereum project, please refer to: [ethereum](https://github.com/ethereum) on github.

The overview of organization of project are:

## MyChains
The private ethereum network configuration folder, including:

|   source   | Description |
|:----------:|-------------|
| miner1 | miner1 configuration and startup scripts on Ubuntu OS. |
| miner2 | miner2 configuration and startup scripts on Ubuntu OS. |
| miner_win7 | miner configuration and startup scripts on window 7 OS. |
| node | node configuration and startup scripts running on Raspberry Pi and Tinker board which are enpowered by Debian Linux on ARM. |
| genesis.json | genesis data for private blockchain network initialization. |
| init_miners.sh | miner initialization script to initialize miner configuration given 'genesis.json' |
| init_node.sh | node initialization script to initialize node configuration given 'genesis.json' |
| static-nodes.json | record all paired static nodes information for private entereum network. |
| Setup_private_Ethereum_network_with_IoT_devices.pdf | Turorials to instruct how to setup private Ethereum network including computers and Raspberry pi. |
	
## Projects
The BlendCAC development project including:

|   source   | Description |
|:----------:|-------------|
| CapbilityToken | truffle project folder to develop smart contract using soliditon. |
| SmartToken | truffle project folder to develop demo contract using soliditon. |
| py_dev | Bolckchain enabled access control strategy by using python. |

## Environment Setup	
The environement configuration includs: Prerequisite, Ethereum Blockchain setup and Smart Contract Development toolkit. Refer to env_setup.txt for detail.

--- env_setup.txt: The blockchain network and application development environment setup instruction.
