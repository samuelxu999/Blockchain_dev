pragma solidity ^0.4.18;

contract CapACToken {

	/*
		Define struct to represent capability token data.
	*/
	struct CapabilityToken {
		uint id;				// token id
		bool initialized;		//check whether token has been initialized
		bool isValid;			// flage to indicate whether token valid, used for temporary dispense operation
		address[5] delegatee; 		// person delegated to access right
		uint delegateDepth; 		// person delegated to access right
		uint256 issuedate;		// token issued date
		uint256 expireddate;		// token expired date
		string authorization;
	}

	// Global state variables
	address private constant supervisor = 0x3d40fad73c91aed74ffbc1f09f4cde7cce533671;
	mapping(address => CapabilityToken) captokens;

	// event handle function
	event OnValueChanged(address indexed _from, uint _value);

	/* 
		function: query token data given address and return general token data
	*/
	function getCapTokenStatus(address recipient) public constant returns (uint, 
																			bool, 
																			bool, 
																			uint256, 
																			uint256) {
		// querying token from authorized address is allowed: supervisor or delegatee
        //if( (recipient == msg.sender) || (supervisor == msg.sender) ) {
		    //var token_str='';
			/*if(captokens[recipient].initialized == false) {
				//tokenToString(recipient);
				iniCapToken(recipient);
			}*/

			return(	captokens[recipient].id, 
					captokens[recipient].initialized,
					captokens[recipient].isValid,
					captokens[recipient].issuedate,
					captokens[recipient].expireddate
					);
		/*}
		// otherwise, return empty data
		else {
			return(	0, 
					false,
					false,
					captokens[recipient].delegatee,
					0,
					0,
					"Empty"
					);
		}*/

	}

	/* 
		function: query delegation data given address
	*/
	function getDelegateStatus(address recipient) public constant returns (uint, address[5], uint) {

			return(	captokens[recipient].id, 
					captokens[recipient].delegatee,
					captokens[recipient].delegateDepth
					);
	}

	/* 
		function: query Authorization data given address
	*/
	function getAuthorization(address recipient) public constant returns (uint, string) {

			return(	captokens[recipient].id, 
					captokens[recipient].authorization
					);
	}


	/*
	Function: Initilized token data given address.
	*/
	function initCapToken(address recipient) public returns (bool) {
		if( supervisor == msg.sender) {
			//set id and initialized flag
			captokens[recipient].id = 1;
			captokens[recipient].initialized = true;

			//disable token
			captokens[recipient].isValid = false;

			//disable delegation
			for(uint i = 0; i < 5; i++) {
				captokens[recipient].delegatee[i] = address(0);
			}
			captokens[recipient].delegateDepth = 0;
			//captokens[recipient].issuedate = now;
			//captokens[recipient].expireddate = now + 1 days;

			//set default access right
			//captokens[recipient].authorization = "No Access Authorized";	

			// notify OnValueChanged event
			OnValueChanged(recipient, captokens[recipient].id);	
			return true;

		}
		else {
			return false;
		}
	}

	// Set isValid flag call function
	function setCapToken_isValid(address recipient, bool isValid) public returns (bool) {
		if( supervisor == msg.sender) {
			captokens[recipient].id += 1;
			captokens[recipient].isValid = isValid;
			OnValueChanged(recipient, captokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}

	// Set delegation depth flag call function
	function setCapToken_delegateDepth(address recipient, uint depth) public returns (bool) {
		if( supervisor == msg.sender) {
			captokens[recipient].id += 1;

			//check if delegation depth is more that max 5
			if(depth > 5) {
				captokens[recipient].delegateDepth = 5;
			}
			else {
				captokens[recipient].delegateDepth = depth;			
			}
			
			OnValueChanged(recipient, captokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}

	// Add delegatee call function
	function setCapToken_delegatee(address recipient, address delegatee) public returns (bool) {
		bool ret = false;
		if( supervisor == msg.sender) {
			uint free_index = 0;
			for(free_index = 0; free_index < captokens[recipient].delegateDepth; free_index++) {
				//check if the address is not set
				if(captokens[recipient].delegatee[free_index] == address(0)) {
					break;
				}
			}
			if(free_index < captokens[recipient].delegateDepth) {
				captokens[recipient].id += 1;
				captokens[recipient].delegatee[free_index] = delegatee;
				OnValueChanged(recipient, captokens[recipient].id);
				ret = true;
			}
		}
		return ret;		
	}

	// revoke delegatee call function
	function setCapToken_revokeDelegate(address recipient, address delegatee) public returns (bool) {
		bool ret = false;
		if( supervisor == msg.sender) {
			uint free_index = 0;
			for(free_index = 0; free_index < captokens[recipient].delegateDepth; free_index++) {
				//check if the address is exist
				if(captokens[recipient].delegatee[free_index] == delegatee) {
					break;
				}
			}
			if(free_index < captokens[recipient].delegateDepth) {
				captokens[recipient].id += 1;
				captokens[recipient].delegatee[free_index] = address(0);
				OnValueChanged(recipient, captokens[recipient].id);
				ret = true;
			}
		}
		return ret;		
	}


	// Set time limitation call function
	function setCapToken_expireddate(address recipient, 
									uint256 issueddate, 
									uint256 expireddate) public returns (bool) {
		if( supervisor == msg.sender) {
			captokens[recipient].id += 1;
			captokens[recipient].issuedate = issueddate;
			captokens[recipient].expireddate = expireddate;
			OnValueChanged(recipient, captokens[recipient].id);
			return true;
		}
		else {
			return false;
		}
	}

	// Set accessright call function
	function setCapToken_authorization(address recipient, 
										string accessright) public returns (bool) {
		if( supervisor == msg.sender) {
			captokens[recipient].id += 1;
			captokens[recipient].authorization = accessright;
			OnValueChanged(recipient, captokens[recipient].id);
			return true;
		}
		else{
			return false;
		}
		
	}
}
