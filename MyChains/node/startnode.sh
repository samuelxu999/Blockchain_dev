#!/bin/bash

geth --identity "node1" --fast --networkid 42 --datadir /home/pi/Desktop/Github/Blockchain_dev/MyChains/node --nodiscover --rpc --rpcport "8042" --port "30303" --unlock 0 --password "/home/pi/Desktop/Github/Blockchain_dev/MyChains/node/password.sec" --ipcpath /home/pi/.ethereum/geth.ipc
