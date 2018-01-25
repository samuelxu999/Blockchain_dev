#!/bin/bash

#Delete chaindata for miners
rm -rf miner1/geth
rm -rf miner2/geth

#Initialize miners
geth --datadir ./miner1 init genesis.json
geth --datadir ./miner2 init genesis.json
