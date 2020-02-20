#!/bin/bash

geth --identity "miner2" \
--networkid 42 \
--datadir "~/Desktop/Github/Blockchain_dev/MyChains/miner2" \
--nodiscover \
--mine \
--minerthreads "1" \
--rpc --rpcport "8043" \
--port "30304" \
--allow-insecure-unlock \
--unlock 0 \
--password ~/Desktop/Github/Blockchain_dev/MyChains/miner2/password.sec
