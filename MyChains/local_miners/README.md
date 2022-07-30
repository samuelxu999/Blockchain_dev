## local_miners
The private ethereum network on single host machine, including:

### miner1
miner1 configuration and startup scripts on Ubuntu OS or mac. 

--- startminer1.sh: start up ethereum client as miner1, ipc-8042, port-30303.

--- node_data:

    --- genesis.json: genesis data for private blockchain network initialization.

    --- password.sec: default password for miner's account.

    --- static-nodes.json: paired static nodes information for miner1 on private entereum network.

### miner2
miner2 configuration and startup scripts on OS or mac. 

--- startminer2.sh: start up ethereum client as miner2, pc-8043, port-30304.

--- node_data:

	--- genesis.json: genesis data for private blockchain network initialization.

	--- password.sec: default password for miner's account.

	--- static-nodes.json: paired static nodes information for miner2 on private entereum network.

### Launch miners
Startup miner1: open a new terminal, then execute `cd miner1; ./startnode.sh`

Startup miner2: open a new terminal, then execute `cd miner2; ./startnode.sh`

### Attach to console
Attach miner1 console: `geth attach miner1/account/geth.ipc`

Attach miner2 console: `geth attach miner2/account/geth.ipc`

### get enode or peer information
After attach console, run following commands to get information:

> eth.accounts									(list all accounts)

> admin.nodeInfo.enode							(show enode data)

> admin.peers									(Show peers information)

> miner.start(1)								(Using 1 code to mine blocks)

> miner.stop()									(Stop mining blocks)

> web3.fromWei(eth.getBalance(eth.coinbase))	(Display mined ether coins)

> eth.blockNumber								(Show total blocks)

Transfer coins between accounts:
> eth.sendTransaction({from:eth.coinbase, to:"0xa79fd8f95fe0cfaf4536ed6292b9388355d39842", value:web3.toWei(100,"ether")})

