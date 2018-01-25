#!/bin/bash

geth --identity "miner1" --networkid 42 --datadir "~/Desktop/Github/Blockchain_dev/MyChains/miner1" --nodiscover --mine --rpc --rpcport "8042" --port "30303" --unlock 0 --password ~/Desktop/Github/Blockchain_dev/MyChains/miner1/password.sec --ipcpath "~/.ethereum/geth.ipc"
