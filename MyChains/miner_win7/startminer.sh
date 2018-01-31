#!/bin/bash

geth --identity "miner_win7" --networkid 42 --datadir "/d/Github/Blockchain_dev/MyChains/miner_win7" --nodiscover --mine --rpc --rpcport "8042" --port "30303" --unlock 0 --password /d/Github/Blockchain_dev/MyChains/miner_win7/password.sec
