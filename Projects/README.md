## Projects
The BlendCAC project folder, including smart contract and access control application development.

Please refer to [Truffle](https://truffleframework.com/docs) for truffle environment setup and usage.

### SmartToken
The truffle project folder to develop demo smart contract illustrated in instruction.
|   source   | Description |
|:----------:|-------------|
| contract | smart contract source code writen in soliditon. |
| migrations | migration (deployment) scripts for smart contract. |
| test |  test code written in Solidity which ensures that your contract is working as expected. |
| truffle-config.js | This is the Truffle configuration file to customize your Truffle configuration. |
| truffle.js | This is the Truffle configuration file, for setting network information and other project-related settings. |

### CapbilityToken
The truffle project folder to develop smart contract for BlendCAC implementation.
* contract:
	--- ABACToken.sol: Arrtibute-based Access Control smart contract.
	--- CapACToken.sol: Capability-based Access Control smart contract.
	--- RBACToken.sol: Role-based Access Control smart contract.
	--- DelegateToken.sol: Federated capability-based delegation smart contract.
	--- Migrations.sol: This is a separate Solidity file that manages and updates the status of your deployed smart contract. This file comes with every Truffle project, and is usually not edited.
	
* migrations:
	--- 1_initial_migration.js: This file is the migration (deployment) script for the Migrations contract found in the Migrations.sol file.
	--- 2_deploy_contracts.js: This file is the migration (deployment) script for deploying our developed smart contract Solidity files.
	
* test:
	--- addr_list.json: This file provide nodename->address mapping table to manage our test nodes in private blockchain network.
	--- utilities.js: This javascripts offers all utility class for test code.
	--- test_token.js: This is a javascripts test file to interact with deployed smart contracts.
 

### py_dev
The prototype desgin of BlednCAC access control strategy by using python. 
* ABAC_Policy.py: This module provide Attribute based AC token struct model and encapsulation of access control policy.
* ABAC_Token.py: This module provide encapsulation of web3.py API to interact with exposed ABI of ABACToken.sol.
* BC_Performance.py: Test functions for blockchain netowrk performance.
* BlendCapAC_Policy.py:This module provide Capability token struct model and encapsulation of access control policy.
* CapAC_Token.py: This module provide encapsulation of web3.py API to interact with exposed ABI of CapACToken.sol.
* Delegate_policy.py:This module provide Delegate token struct model and encapsulation of delegation policy.
* Delegate_Token.py: This module provide encapsulation of web3.py API to interact with exposed ABI of DelegateToken.sol.
* RBAC_Policy.py: This module provide Role based AC token struct model and encapsulation of access control policy.
* RBAC_Token.py: This module provide encapsulation of web3.py API to interact with exposed ABI of RBACToken.sol.
* WS_Client.py: This module provide encapsulation of client API that access to Web service.
* WS_Server.py: This module provide encapsulation of server API that handle and response client's request.
* db_layer.py: This module provide database layer API to interact with SQLite engine.
* measure_performance.py: This module provide performance measure utilities, such as data extract, merge, and visualization.
* utilities.py: This module provide utility functions to support project.
