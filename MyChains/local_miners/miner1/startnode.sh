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

	## Copy password to docker
	cp $Node_dir/password.sec $Account_dir/password.sec

	## Create account based on password.sec
	geth --datadir $Account_dir account new --password $Account_dir/password.sec
fi

## copy static-nodes.json to account folder
cp $Node_dir/static-nodes.json $Account_dir/geth/

## launch geth client app
geth --identity "geth_node" \
--networkid 2104 \
--datadir "$Account_dir" \
--nodiscover \
--syncmode full \
--gcmode archive \
--http --http.port "8042" \
--port "30303" \
--allow-insecure-unlock \
--unlock 0 \
--password "$Account_dir/password.sec"
