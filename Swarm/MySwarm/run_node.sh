#!/bin/bash

# parse parameters
Node_Dir=$1
Account_addr=$2
bzz_Port=$3
port=$4

if  [ "" == "$bzz_Port" ] ; then
	bzz_Port=8500
fi

if  [ "" == "$port" ] ; then
	port=30399
fi

# start swarm node
swarm \
--datadir ./$Node_Dir \
--keystore ./$Node_Dir/keystore \
--password ./$Node_Dir/password.sec \
--bzznetworkid 5 \
--bzzaccount $Account_addr \
--bzzport $bzz_Port \
--port $port
