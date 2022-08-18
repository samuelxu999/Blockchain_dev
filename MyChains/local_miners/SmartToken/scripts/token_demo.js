/*
=========================== This is demo test script to acces our smart token object =======================================
*/

// Interaction with Ethereum
var Web3 = require('web3');
var web3 = new Web3();

// connect to the local node
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8042'));

// The contract that we are going to interact with
var contractAddress = '0xF271F04c0592c7386381E9487A56B968BeDad2fB';

// Load config data from SmartToken.json
var config = require('../build/contracts/SmartToken.json');

// Readin ABI
var ABI = config.abi;

// new a contract object
var contract = new web3.eth.Contract(ABI, contractAddress)


// ======================= test functions for demo ==================================
//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('./addr_list.json');	
	return addrlist[node_name];	
}

// print out local accounts
const printAccounts = async () => {
	// using the promise
	const ls_accounts = web3.eth.getAccounts()
	.then(function(accounts){
		//print out accounts data
		// console.log(accounts);
		return accounts
	});

	// await to get accounts 
	const accounts = await ls_accounts;

	// print all accounts
	console.log('All accounts:');
	for (i = 0; i < accounts.length; i++) { 
		// display one account
		console.log(`[${i+1}] ${accounts[i]}`);
	}
};


// call getTokens to read value of a node address 
function get_token(node_name) {
	var address=getAddress(node_name);
	
	// using the promise
	contract.methods.getTokens(address).call({from: '0x9374E09e81d54c190Cd94266EaaD0F2A2b060AF6'})
	.then(function(result){
		//print out tracsaction result
		console.log(`address: ${address}, value: ${result}`);
	});

}

// send depositToken transaction
function deposit_test(node_name, value) {
	var recipient=getAddress(node_name);
	// using the promise
	contract.methods.depositToken(recipient, value).send({from: '0x9374E09e81d54c190Cd94266EaaD0F2A2b060AF6'})
	.then(function(receipt){
		//print out result data
		console.log(receipt);
	});
}

// send withdrawToken transaction
function withdraw_test(node_name, value) {
	var recipient=getAddress(node_name);
	// using the promise
	contract.methods.withdrawToken(recipient, value).send({from: '0x9374E09e81d54c190Cd94266EaaD0F2A2b060AF6'})
	.then(function(receipt){
		//print out tracsaction result
		console.log(receipt);
	});
}


//================================= test demo ==================================
const myArgs = process.argv.slice(2);

// var test_node = "node1_0";
var test_node = myArgs[1];
var token_value = myArgs[2];

switch (myArgs[0]) {
  case '0':
    printAccounts()
    break;
  case '1':
    get_token(test_node);
    break;
  case '2':
    deposit_test(test_node, token_value);
    break;
  case '3':
    withdraw_test(test_node, token_value);
    break;
  default:
    console.log("run sample: node scripts/token_demo.js 1 node1_0");
}
