/*
=========================== This is demo test script to acces our smart token object =======================================
*/

// Interaction with Ethereum
var Web3 = require('web3');
var web3 = new Web3();

// connect to the local node
web3.setProvider(new web3.providers.HttpProvider('http://127.0.0.1:8042'));

// The contract that we are going to interact with
var contractAddress = '0x9a9977070eBfc13f6AA5CEf755268BB08BBb604d';

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
};

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
const get_token = async (node_name) => {
	// using the promise to get accounts
	const ls_accounts = web3.eth.getAccounts()
	.then(function(accounts){
		//print out accounts data
		// console.log(accounts);
		return accounts
	});

	// await to get accounts 
	const accounts = await ls_accounts;

	// get coinbase account
	var coinbase = accounts[0];

	// get node address
	var address=getAddress(node_name);

	// using the promise to call getTokens()
	contract.methods.getTokens(address).call({from: coinbase})
	.then(function(result){
		//print out tracsaction result
		console.log(`address: ${address}, value: ${result}`);
	});

};

// send depositToken transaction
const deposit_test = async (node_name, value) => {
	// using the promise to get accounts
	const ls_accounts = web3.eth.getAccounts()
	.then(function(accounts){
		//print out accounts data
		// console.log(accounts);
		return accounts
	});

	// await to get accounts 
	const accounts = await ls_accounts;

	// get coinbase account
	var coinbase = accounts[0];

	// get node address
	var recipient=getAddress(node_name);

	// using the promise to send depositToken()
	contract.methods.depositToken(recipient, value).send({from: coinbase})
	.then(function(receipt){
		//print out result data
		console.log(receipt);
	});
};

// send withdrawToken transaction
const withdraw_test = async (node_name, value) => {
	// using the promise to get accounts
	const ls_accounts = web3.eth.getAccounts()
	.then(function(accounts){
		//print out accounts data
		// console.log(accounts);
		return accounts
	});

	// await to get accounts 
	const accounts = await ls_accounts;

	// get coinbase account
	var coinbase = accounts[0];

	// get node address
	var recipient=getAddress(node_name);

	// using the promise to send withdrawToken()
	contract.methods.withdrawToken(recipient, value).send({from: coinbase})
	.then(function(receipt){
		//print out tracsaction result
		console.log(receipt);
	});
};

//================================= test demo ==================================
// readin arguments from CLI
const myArgs = process.argv.slice(2);

// set test_node and token_value;
var test_node = myArgs[1];
var token_value = myArgs[2];

// switch to test cases
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
};