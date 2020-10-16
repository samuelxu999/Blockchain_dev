#!/bin/bash

# node directory path
Node_Dir=$1

# create node dir if not exist
mkdir ./$Node_Dir

#Copy password to node dir
cp ./password.sec ./$Node_Dir/password.sec

# New a ethereum account
geth --datadir ./$Node_Dir account new --password ./$Node_Dir/password.sec
