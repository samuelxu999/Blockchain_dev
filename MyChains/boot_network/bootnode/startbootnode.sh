#!/bin/sh

## Set key folder path
KEY_DIR="./account/keystore"
Account_dir="./account"
Node_dir="./node_data"

## check if main account is available
if ! [ "$(/bin/ls -A $KEY_DIR)" ]; then
	## new account dir
	mkdir $Account_dir

	## Initialize miners
	geth --datadir $Account_dir init $Node_dir/genesis.json

fi

## launch geth client app
bootnode --genkey boot.key

bootnode --nodekey boot.key --addr ":39301" 
