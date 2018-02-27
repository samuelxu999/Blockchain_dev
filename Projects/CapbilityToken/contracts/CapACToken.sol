pragma solidity ^0.4.18;

contract CapACToken {

	/*
		Define struct to represent capability token data.
	*/
	struct CapabilityToken {
		uint id;				// token id
		bool initialized;		//check whether token has been initialized
		bool isValid;			// flage to indicate whether token valid, used for temporary dispense operation
		address delegatee; 		// person delegated to access right
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
		function: query token data given address and return token data
	*/
	function getCapToken(address recipient) public constant returns (uint, 
																	bool, 
																	bool, 
																	address, 
																	uint256, 
																	uint256, 
																	string) {
		// querying token from authorized address is allowed: supervisor or delegatee
        if( (recipient == msg.sender) || (supervisor == msg.sender) ) {
		    //var token_str='';
			/*if(captokens[recipient].initialized == false) {
				//tokenToString(recipient);
				iniCapToken(recipient);
			}*/

			return(	captokens[recipient].id, 
					captokens[recipient].initialized,
					captokens[recipient].isValid,
					captokens[recipient].delegatee,
					captokens[recipient].issuedate,
					captokens[recipient].expireddate,
					captokens[recipient].authorization
					);
		}
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
		}

	}

	/*
	Function: Initilized token data given address.
	*/
	function initCapToken(address recipient) public returns (bool) {
		if( supervisor == msg.sender) {
			//set id and initialized flag
			captokens[recipient].id = 1;
			captokens[recipient].initialized = true;

			//set token information
			captokens[recipient].isValid = false;
			captokens[recipient].delegatee = recipient;
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
