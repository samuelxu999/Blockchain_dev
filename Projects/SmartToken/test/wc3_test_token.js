/*
=========================== This is demo test script to acces our smart token object =======================================
*/

// Interaction with Ethereum
var Web3 = require('web3')
var web3 = new Web3()

// connect to the local node
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8042'))

// The contract that we are going to interact with
var contractAddress = '0x1987802daa5798cfb5e881c109c4d448b6e4125b'

// Load config data from SmartToken.json
var config = require('../build/contracts/SmartToken.json');

// Read ABI
var ABI = config.abi;

// Define the ABI (Application Binary Interface)
//var ABI = JSON.parse('[ { "constant": false, "inputs": [ { "name": "recipient", "type": "address" }, { "name": "value", "type": "uint256" } ], "name": "depositToken", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "recipient", "type": "address" } ], "name": "getTokens", "outputs": [ { "name": "value", "type": "uint256", "value": "60" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "recipient", "type": "address" }, { "name": "value", "type": "uint256" } ], "name": "withdrawToken", "outputs": [ { "name": "success", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_from", "type": "address" }, { "indexed": false, "name": "_value", "type": "uint256" } ], "name": "OnValueChanged", "type": "event" } ]')

// contract object
var contract = web3.eth.contract(ABI).at(contractAddress)

//-------------------------- test demo -------------------------------
var test_node = "node1_1";

//list value in all account
//list_all();
get_token(test_node);

//deposit_test(getAddress(test_node), 3)
withdraw_test(getAddress(test_node), 2);

// display initial state
//showStatus()

//get_token('miner1_1');
var address=getAddress(test_node);
account_onValueChanged(address);


//====================================== function for test ==================================
// wait for an event triggered on the Smart Contract
function account_onValueChanged(address) {
	var onValueChanged = contract.OnValueChanged({_from: address});

	onValueChanged.watch(function(error, result) {
		if (!error) {
			//showStatus()
			var token = contract.getTokens(address);
			console.log(token);
		}
	})
}

// display value of the token in coinbase account
function showStatus() {
 
	// retrieve the value of the token
	var token = contract.getTokens(web3.eth.coinbase)

	// display the value of the token in accounts[0]
	console.log(token);

}

// list all local count token data
function list_all() {
	/*var add1='0xaa09c6d65908e54bf695748812c51d8f2ceea0f5';
	var add2='0x950d8eb4825c597534027638c862496ea0d7cf43';*/
	
	for (i = 0; i < web3.eth.accounts.length; i++) { 
		// get token value 
		var token = contract.getTokens(web3.eth.accounts[i])
		// display the value of the token according to account
		console.log(token);
	}
}

function get_token(node_name) {
	var address=getAddress(node_name)
	var token = contract.getTokens(address)
	console.log(token);
}

// launch depositToken transaction
function deposit_test(recipient, value) {
	var ret=contract.depositToken(recipient, value, {from: web3.eth.coinbase})
	// display the tracsaction result
	console.log(ret);
}

// launch withdrawToken transaction
function withdraw_test(recipient, value) {
	var ret=contract.withdrawToken(recipient, value, {from: web3.eth.coinbase})
	// display the tracsaction result
	console.log(ret);
}

//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('./addr_list.json');	
	return addrlist[node_name];	
}

