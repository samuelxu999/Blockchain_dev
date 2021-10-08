#!/bin/bash

# parse parameters
Node_Dir=$1
bzz_Port=$2
port=$3

## --------------- if Node_Dir is not exist, new one ----------
if [ ! -d "$Node_Dir" ]; then
	echo "Directory '$Node_Dir' is not existed, create it."
	mkdir "$Node_Dir"
fi

## -------------- If there is no account, create one --------------
if [ -z "$(ls -A $Node_Dir)" ]; then
    echo "Empty account, new an ethereum account"
	## Copy password to node dir
	cp password.sec $Node_Dir/password.sec

	## New an ethereum account
	geth --datadir $Node_Dir account new --password $Node_Dir/password.sec

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
echo $account_address

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

## start swarm node
swarm \
--datadir $Node_Dir \
--keystore $Node_Dir/keystore \
--password $Node_Dir/password.sec \
--bzznetworkid 5 \
--bzzaccount $account_address \
--bzzport $bzz_Port \
--port $port
