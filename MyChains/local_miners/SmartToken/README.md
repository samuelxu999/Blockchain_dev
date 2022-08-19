# Sample truffle Project for learning process

This project demonstrates a basic smart contract use case. It comes with a sample contract, a test for that contract, and a script that deploys that contract.

Try running some of the following truffle and unit test tasks:

```shell
// install dependencies
npm install

// compile contracts
truffle compile	

// deploy contracts on local network (enable networks->development in truffle-config.js)
truffle migrate --reset

// execute unit test cases (disable networks->development in truffle-config.js)
truffle test
```

Before running demo cases:
-- ensure local miners are running
-- enable networks->development in truffle-config.js
-- migrate contract to test network
-- update deployed contract address in "SmartToken" of 'addr_list.json' 

```shell
// execute demo test cases (js)
node scripts/token_demo.js X   					//get usages
node scripts/token_demo.js 0
node scripts/token_demo.js 1 node1_0
node scripts/token_demo.js 2 node1_0 5
node scripts/token_demo.js 2 node1_0 3

// execute demo test cases (py)
python3 token_demo.py -h  						// get usages
python3 token_demo.py --test_op 0
python3 token_demo.py --test_op 1 --id node1_1
python3 token_demo.py --test_op 2 --id node1_1 --value 5
python3 token_demo.py --test_op 3 --id node1_1 --value 3
```
