## MyChains
The private ethereum network configuration folder, including:

### miner1
miner1 configuration and startup scripts on Ubuntu OS. 
--- startminer1.sh: start up ethereum client as miner1.
--- static-nodes.json: paired static nodes information for miner1 on private entereum network.

### miner2
miner2 configuration and startup scripts on Ubuntu OS. 
--- startminer2.sh: start up ethereum client as miner2.
--- static-nodes.json: paired static nodes information for miner2 on private entereum network.

### miner_win7
miner configuration and startup scripts on window 7 OS. 
--- startminer.sh: start up ethereum client as miner on window 7 system.

### node
node configuration and startup scripts running on Raspberry Pi and Tinker board which are enpowered by Debian Linux on ARM.
--- startnode.sh: start up ethereum client as node without executing mining task on host machine.
--- static-nodes.json: paired static nodes information for node on private entereum network.

### genesis.json 
genesis data for private blockchain network initialization.

### init_miners.sh 
miner initialization script to initialize miner configuration given 'genesis.json'.

### init_node.sh
node initialization script to initialize node configuration given 'genesis.json'.

### static-nodes.json
Global record for all paired static nodes information on private entereum network. Copy all or part of static nodes information to each miner# or node# folder to configurate pared nodes.

### Setup_private_Ethereum_network_with_IoT_devices.pdf
Turorials to instruct how to setup private Ethereum network including computers and Raspberry pi.