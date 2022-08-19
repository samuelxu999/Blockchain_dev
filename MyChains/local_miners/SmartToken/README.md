# Sample truffle Project for learning process

This project demonstrates a basic smart contract use case. It comes with a sample contract, a test for that contract, and a script that deploys that contract.

Try running some of the following tasks:

```shell
// install dependencies
npm install

// compile contracts
truffle compile	

// deploy contracts on local network (enable networks->development in truffle-config.js)
truffle migrate --reset

// execute unit test cases (disable networks->development in truffle-config.js)
truffle test

// execute demo test cases (ensure local miners are running and enable networks->development in truffle-config.js)
node scripts/token_demo.js 1 node1_0
```
