#!/bin/bash


## ports from argv
bzz_Port=$1
port=$2

## node directory path
Node_Dir="/home/docker/swarm/node"
geth_bin="/opt/go_proj/src/github.com/ethereum/go-ethereum/build/bin"
swarm_bin="/opt/go_proj/src/github.com/ethereum/swarm/build/bin"


## -------------- If there is no account, create one --------------
if [ -z "$(ls -A $Node_Dir)" ]; then
   /bin/echo "Empty account, new an ethereum account"
	## Copy password to node dir
	/bin/cp /home/docker/swarm/cmd/password.sec $Node_Dir/password.sec

	## New an ethereum account
	$geth_bin/geth --datadir $Node_Dir account new --password $Node_Dir/password.sec

	/bin/sleep 2
fi

## split key file to get account address
for entry in "$Node_Dir/keystore"/*
	do
	# echo "$entry"
	key_file=$(basename "$entry")
done

## -------------------- get account address ------------------------
## Set -- as the delimiter
IFS='--'

## Read the split words into an array based on space delimiter
read -a strarr <<< "$key_file"

## Count the lenght of split words
arrlen=${#strarr[*]}
# echo $arrlen

## using last work as account_address
account_address="${strarr[$arrlen-1]}"
/bin/echo $account_address


## ------------- verify port before run swarm node ----------------------
if  [ "" == "$bzz_Port" ] ; then
	bzz_Port=8500
elif ! [[ $bzz_Port =~ ^[0-9]+$ ]]; then
	/bin/echo "Error: rpcport should be integer!"
	exit 0	
fi

if  [ "" == "$port" ] ; then
	port=30399
elif ! [[ $port =~ ^[0-9]+$ ]]; then
	/bin/echo "Error: port should be integer!"
	exit 0	
fi

## ----------------------- run swarm node ------------------------------
$swarm_bin/swarm \
--datadir $Node_Dir \
--keystore $Node_Dir/keystore \
--password $Node_Dir/password.sec \
--bzznetworkid 5 \
--bzzaccount $account_address \
--bzzport $bzz_Port \
--port $port


