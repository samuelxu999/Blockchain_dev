pragma solidity ^0.4.18;

//Attribute-based Access Control model
contract ABACToken {

	/*
		Define struct to represent role based token data.
	*/
	struct AttributeToken {
		uint id;					// token id
		bool initialized;			// check whether token has been initialized
		bool isValid;				// flage to indicate whether token valid, used for temporary dispense operation
		address[5] delegatee; 		// person delegated to access right
		uint delegateDepth; 		// maximum delegation operations
		uint256 issuedate;			// token issued date
		uint256 expireddate;		// token expired date
		string attribute;			// Attribute assined to user	
	}

	// Global state variables
	address private constant supervisor = 0x3d40fad73c91aed74ffbc1f09f4cde7cce533671;
	mapping(address => AttributeToken) attributetokens;

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

			return(	attributetokens[recipient].id, 
					attributetokens[recipient].initialized,
					attributetokens[recipient].isValid,
					attributetokens[recipient].issuedate,
					attributetokens[recipient].expireddate
					);

	}

	/* 
		function: query delegation data given address
	*/
	function getDelegateStatus(address recipient) public constant returns (uint, address[5], uint) {

			return(	attributetokens[recipient].id, 
					attributetokens[recipient].delegatee,
					attributetokens[recipient].delegateDepth
					);
	}

	/* 
		function: query Role data given address
	*/
	function getAttribute(address recipient) public constant returns (uint, string) {

			return(	attributetokens[recipient].id, 
					attributetokens[recipient].attribute
					);
	}


	/*
	Function: Initilized token data given address.
	*/
	function initAttributeToken(address recipient) public returns (bool) {
		if( supervisor == msg.sender) {
			//set id and initialized flag
			attributetokens[recipient].id = 1;
			attributetokens[recipient].initialized = true;

			//disable token
			attributetokens[recipient].isValid = false;

			//disable delegation
			for(uint i = 0; i < 5; i++) {
				attributetokens[recipient].delegatee[i] = address(0);
			}
			attributetokens[recipient].delegateDepth = 0;

			// notify OnValueChanged event
			OnValueChanged(recipient, attributetokens[recipient].id);	
			return true;

		}
		else {
			return false;
		}
	}

	// Set isValid flag call function
	function setAttributeToken_isValid(address recipient, bool isValid) public returns (bool) {
		if( supervisor == msg.sender) {
			attributetokens[recipient].id += 1;
			attributetokens[recipient].isValid = isValid;
			OnValueChanged(recipient, attributetokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}

	// Set delegation depth flag call function
	function setAttributeToken_delegateDepth(address recipient, uint depth) public returns (bool) {
		if( supervisor == msg.sender) {
			attributetokens[recipient].id += 1;

			//check if delegation depth is more that max 5
			if(depth > 5) {
				attributetokens[recipient].delegateDepth = 5;
			}
			else {
				attributetokens[recipient].delegateDepth = depth;			
			}
			
			OnValueChanged(recipient, attributetokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}

	// Add delegatee call function
	function setAttributeToken_delegatee(address recipient, address delegatee) public returns (bool) {
		bool ret = false;
		if( supervisor == msg.sender) {
			uint free_index = 0;
			for(free_index = 0; free_index < attributetokens[recipient].delegateDepth; free_index++) {
				//check if the address is not set
				if(attributetokens[recipient].delegatee[free_index] == address(0)) {
					break;
				}
			}
			if(free_index < attributetokens[recipient].delegateDepth) {
				attributetokens[recipient].id += 1;
				attributetokens[recipient].delegatee[free_index] = delegatee;
				OnValueChanged(recipient, attributetokens[recipient].id);
				ret = true;
			}
		}
		return ret;		
	}

	// revoke delegatee call function
	function setAttributeToken_revokeDelegate(address recipient, address delegatee) public returns (bool) {
		bool ret = false;
		if( supervisor == msg.sender) {
			uint free_index = 0;
			for(free_index = 0; free_index < attributetokens[recipient].delegateDepth; free_index++) {
				//check if the address is exist
				if(attributetokens[recipient].delegatee[free_index] == delegatee) {
					break;
				}
			}
			if(free_index < attributetokens[recipient].delegateDepth) {
				attributetokens[recipient].id += 1;
				attributetokens[recipient].delegatee[free_index] = address(0);
				OnValueChanged(recipient, attributetokens[recipient].id);
				ret = true;
			}
		}
		return ret;		
	}


	// Set time limitation call function
	function setAttributeToken_expireddate(address recipient, 
									uint256 issueddate, 
									uint256 expireddate) public returns (bool) {
		if( supervisor == msg.sender) {
			attributetokens[recipient].id += 1;
			attributetokens[recipient].issuedate = issueddate;
			attributetokens[recipient].expireddate = expireddate;
			OnValueChanged(recipient, attributetokens[recipient].id);
			return true;
		}
		else {
			return false;
		}
	}

	// Set role call function
	function setAttributeToken_Attribute(address recipient, string attribute) public returns (bool) {
		if( supervisor == msg.sender) {
			attributetokens[recipient].id += 1;
			attributetokens[recipient].attribute = attribute;
			OnValueChanged(recipient, attributetokens[recipient].id);
			return true;
		}
		else{
			return false;
		}		
	}
}
