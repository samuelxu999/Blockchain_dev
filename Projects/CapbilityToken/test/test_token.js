/*
=========================== This is demo test script to acces our smart token object =======================================
*/

// Interaction with Ethereum
var Web3 = require('web3');
const myUtility = require('./utilities');
var web3 = new Web3();

// connect to the local node
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8042'));

// The contract address that we are going to interact with
var contractAddress = '0x9ccaa35b84570597fce4db8b157ae5cebfb4d0e5';

// Load node addresses data from SmartToken.json
var config = require('../build/contracts/CapACToken.json');

// Read ABI(Application Binary Interface)
var ABI = config.abi;

// new contract object according to ABI and address
var contract = web3.eth.contract(ABI).at(contractAddress);

//-------------------------- test demo -------------------------------
var test_node = "sam_miner_win7_0";


//read token data before transaction
get_token(test_node);


//setToken_test(getAddress(test_node), 11, true, '{"resource":"/test/api/v1.0/dt","action":"GET","conditions":{"value":{"start":"8:12:32"}}');
setToken_test(getAddress(test_node));

//bind event onChange
var address = getAddress(test_node);
account_onValueChanged(address);

//test_fun()


//====================================== function for test ==================================
// wait for an event triggered on the Smart Contract
function account_onValueChanged(address) {
	var onValueChanged = contract.OnValueChanged({_from: address});

	//open watching.
	onValueChanged.watch(function(error, result) {
		if (!error) {
			//showStatus()
			var token = contract.getCapToken(address);
			console.log(token);

			//stop watching
			onValueChanged.stopWatching();
		}
	})
}

function get_token(node_name) {
	var address=getAddress(node_name);
	var token = contract.getCapToken(address);

	for (var i = 0; i <token.length; i++) {
		if(i!=4 && i!=5) {
			console.log(token[i]);
		}
		else {
			//console.log(token[i].c[0]);
			expdate = myUtility.Datetime.IntToDate(token[i].c[0]);
			console.log(myUtility.Datetime.FormatString(expdate));
		}
	}

	//print out token data
	//console.log(token.s);
	//console.log(token.e);
	//console.log(token["c"][0]);
}

// launch depositToken transaction
function setToken_test(recipient) {
	// initialize token
	//var ret=contract.initCapToken( recipient, {from: web3.eth.coinbase} );

	// change isValid flag in token
	//var ret=contract.setCapToken_isValid(recipient, true, {from: web3.eth.coinbase});

	// set issue date and expired date
	/*var nowtime = new Date();
	var issue_time = myUtility.Datetime.DateToInt(nowtime);
	var expire_time = myUtility.Datetime.DateToInt(myUtility.Datetime.DateAdd(nowtime, 1, EumDateType.Months))
	var ret=contract.setCapToken_expireddate(recipient, issue_time, expire_time, {from: web3.eth.coinbase});*/

	// set access right
	var access_right='{"resource":"/test/api/v1.0/dt, "action":"GET"}';
	//var access_right='{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}';
	var ret=contract.setCapToken_authorization(recipient, access_right, {from: web3.eth.coinbase});

	// display the tracsaction result
	console.log(ret);
}

//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('./addr_list.json');	
	return addrlist[node_name];	
}


function test_fun() {
	var nowtime = new Date();
	console.log(myUtility.Datetime.FormatString(nowtime));
	var num_date = myUtility.Datetime.DateToInt(nowtime);
	console.log(num_date);

	console.log(myUtility.Datetime.IntToDate(num_date));

	//change token data
	/*var data = require('./token_data.json');
	var json_string = JSON.stringify(data.access_right[0]);
	//console.log(data.access_right)
	//console.log(data.access_right[0].conditions);
	console.log(json_string)*/

	//
	var startDate = new Date();
	var newdate = myUtility.Datetime.DateAdd(startDate, 1, EumDateType.Months)
	console.log(startDate);
	console.log(newdate);

}

