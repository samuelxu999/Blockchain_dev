pragma solidity ^0.4.18;

//Role-based Access Control model
contract RBACToken {

	/*
		Define struct to represent role based token data.
	*/
	struct RoleToken {
		uint id;					// token id
		bool initialized;			// check whether token has been initialized
		bool isValid;				// flage to indicate whether token valid, used for temporary dispense operation
		address[5] delegatee; 		// person delegated to access right
		uint delegateDepth; 		// maximum delegation operations
		uint256 issuedate;			// token issued date
		uint256 expireddate;		// token expired date
		string role;				// Role assined to user	
	}

	// Global state variables
	address private constant supervisor = 0x3d40fad73c91aed74ffbc1f09f4cde7cce533671;
	mapping(address => RoleToken) roletokens;

	// event handle function
	event OnValueChanged(address indexed _from, uint _value);

	/* 
		function: query token data given address and return general token data
	*/
	function getTokenStatus(address recipient) public constant returns (uint, 
																			bool, 
																			bool, 
																			uint256, 
																			uint256) {

			return(	roletokens[recipient].id, 
					roletokens[recipient].initialized,
					roletokens[recipient].isValid,
					roletokens[recipient].issuedate,
					roletokens[recipient].expireddate
					);

	}

	/* 
		function: query delegation data given address
	*/
	function getDelegateStatus(address recipient) public constant returns (uint, address[5], uint) {

			return(	roletokens[recipient].id, 
					roletokens[recipient].delegatee,
					roletokens[recipient].delegateDepth
					);
	}

	/* 
		function: query Role data given address
	*/
	function getRole(address recipient) public constant returns (uint, string) {

			return(	roletokens[recipient].id, 
					roletokens[recipient].role
					);
	}


	/*
	Function: Initilized token data given address.
	*/
	function initRoleToken(address recipient) public returns (bool) {
		if( supervisor == msg.sender) {
			//set id and initialized flag
			roletokens[recipient].id = 1;
			roletokens[recipient].initialized = true;

			//disable token
			roletokens[recipient].isValid = false;

			//disable delegation
			for(uint i = 0; i < 5; i++) {
				roletokens[recipient].delegatee[i] = address(0);
			}
			roletokens[recipient].delegateDepth = 0;

			// notify OnValueChanged event
			OnValueChanged(recipient, roletokens[recipient].id);	
			return true;

		}
		else {
			return false;
		}
	}

	// Set isValid flag call function
	function setRoleToken_isValid(address recipient, bool isValid) public returns (bool) {
		if( supervisor == msg.sender) {
			roletokens[recipient].id += 1;
			roletokens[recipient].isValid = isValid;
			OnValueChanged(recipient, roletokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}

	// Set delegation depth flag call function
	function setRoleToken_delegateDepth(address recipient, uint depth) public returns (bool) {
		if( supervisor == msg.sender) {
			roletokens[recipient].id += 1;

			//check if delegation depth is more that max 5
			if(depth > 5) {
				roletokens[recipient].delegateDepth = 5;
			}
			else {
				roletokens[recipient].delegateDepth = depth;			
			}
			
			OnValueChanged(recipient, roletokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}

	// Add delegatee call function
	function setRoleToken_delegatee(address recipient, address delegatee) public returns (bool) {
		bool ret = false;
		if( supervisor == msg.sender) {
			uint free_index = 0;
			for(free_index = 0; free_index < roletokens[recipient].delegateDepth; free_index++) {
				//check if the address is not set
				if(roletokens[recipient].delegatee[free_index] == address(0)) {
					break;
				}
			}
			if(free_index < roletokens[recipient].delegateDepth) {
				roletokens[recipient].id += 1;
				roletokens[recipient].delegatee[free_index] = delegatee;
				OnValueChanged(recipient, roletokens[recipient].id);
				ret = true;
			}
		}
		return ret;		
	}

	// revoke delegatee call function
	function setRoleToken_revokeDelegate(address recipient, address delegatee) public returns (bool) {
		bool ret = false;
		if( supervisor == msg.sender) {
			uint free_index = 0;
			for(free_index = 0; free_index < roletokens[recipient].delegateDepth; free_index++) {
				//check if the address is exist
				if(roletokens[recipient].delegatee[free_index] == delegatee) {
					break;
				}
			}
			if(free_index < roletokens[recipient].delegateDepth) {
				roletokens[recipient].id += 1;
				roletokens[recipient].delegatee[free_index] = address(0);
				OnValueChanged(recipient, roletokens[recipient].id);
				ret = true;
			}
		}
		return ret;		
	}


	// Set time limitation call function
	function setRoleToken_expireddate(address recipient, 
									uint256 issueddate, 
									uint256 expireddate) public returns (bool) {
		if( supervisor == msg.sender) {
			roletokens[recipient].id += 1;
			roletokens[recipient].issuedate = issueddate;
			roletokens[recipient].expireddate = expireddate;
			OnValueChanged(recipient, roletokens[recipient].id);
			return true;
		}
		else {
			return false;
		}
	}

	// Set role call function
	function setRoleToken_Role(address recipient, string role) public returns (bool) {
		if( supervisor == msg.sender) {
			roletokens[recipient].id += 1;
			roletokens[recipient].role = role;
			OnValueChanged(recipient, roletokens[recipient].id);
			return true;
		}
		else{
			return false;
		}		
	}
}
