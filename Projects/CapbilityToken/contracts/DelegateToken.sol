pragma solidity ^0.4.18;

contract DelegateToken {

	/*
		Define struct to represent delegation node data.
	*/
	struct Node {
		address parent;				// delegatee address
		address[5] children;		// children nodes, maximum delegation width is 5
		uint depth;					// current node depth
		uint delegateWidth; 		// maximum delegation width: available delegatees
		string privileges;			// delegated privileges
	}

	/*
		Define struct to represent delegation tree data.
	*/
	struct Tree {
		address rootnode;
		uint delegateDepth; 		// maximum delegation progagation depth
		mapping(address => Node) nodes;
	}

	// Global state variables
	address private constant supervisor = 0x3d40fad73c91aed74ffbc1f09f4cde7cce533671;
	Tree private delTree;
	uint private constant MAX_DELEGATE_WIDTH = 5;
	uint private constant MAX_DELEGATE_DEPTH = 3;

	/************************************* tree functions ******************************************/
	function insertNode(address delegator, address delegatee) 
						private returns (bool) {
		// DelegateTree is not initialized
		if(delTree.rootnode == address(0)) 
			return false;
		
		// define empty_slot to record first empty childnode
		uint empty_slot = MAX_DELEGATE_WIDTH;

		// check children nodes
		for(uint i = 0; i < MAX_DELEGATE_WIDTH; i++) {
			//find empty slot
			if(delTree.nodes[delegator].children[i] == address(0)) {
				empty_slot = i;
				break;
			}
		}

		//check whether children nodes are full
		if(empty_slot >= MAX_DELEGATE_WIDTH) {
			return false;
		}

		// add new delegatee address to children
		delTree.nodes[delegator].children[empty_slot] = delegatee;
		
		// update node based on delegatee address
		delTree.nodes[delegatee].parent = delegator;
		delTree.nodes[delegatee].depth = delTree.nodes[delegator].depth + 1;
		//delTree.nodes[delegatee].delegateWidth = delegateWidth;
		//delTree.nodes[delegatee].privileges = privileges;

		return true;
	}

	function removeNode(address id) private returns (bool) {
		// DelegateTree is not initialized
		if(delTree.rootnode == address(0)) 
			return false;
		
		// get parent node
		address parent = delTree.nodes[id].parent;

		// skip root node and empty node
		if(parent == address(0)) 
			return false;

		// remove node from parent's children list
		for(uint i = 0; i < MAX_DELEGATE_WIDTH; i++) { 
			if(delTree.nodes[parent].children[i] == id) {
				delTree.nodes[parent].children[i] = address(0);
				break;
			}
		}

		// clear current node data
		delTree.nodes[id].parent = address(0);
		delTree.nodes[id].depth = 0;
		delTree.nodes[id].delegateWidth = 0;
		delTree.nodes[id].privileges = '';

		// delete associated children nodes
		for(i = 0; i < MAX_DELEGATE_WIDTH; i++) { 
			if(delTree.nodes[id].children[i] == address(0)) 
				continue;

			//delete child
			removeNode(delTree.nodes[id].children[i]);
		}

		return true;
	}

	function isAncestor(address ancestor, address id) private returns (bool) { 
		//get current node depth
		uint depth = delTree.nodes[id].depth;

		//get parent depth
		address parent = delTree.nodes[id].parent;

		// up to root for searching parent
		for(uint i = 0; i < depth; i++) {			
			if(ancestor == parent) {
				return true;
			}
			parent = delTree.nodes[parent].parent;
		}

		return false;
	}


	/************************************* transaction functions ******************************************/
	// initialize delegate tree
	function initTree() public payable returns(bool) {
		if( supervisor != msg.sender) 
			return false;

		// initialize tree
		delTree.rootnode = supervisor;
		delTree.delegateDepth = 1;

		// initialize rootnode
		delTree.nodes[supervisor].parent = address(0);
		delTree.nodes[supervisor].depth = 0;
		delTree.nodes[supervisor].delegateWidth = MAX_DELEGATE_WIDTH;
		delTree.nodes[supervisor].privileges = 'supervisor';

		return true;
	}

	// set tree depth
	function setTreeDepth(uint delegateDepth) public payable returns(bool) {
		if( supervisor != msg.sender) 
			return false;
		
		// set delegateDepth
		if(delegateDepth < MAX_DELEGATE_DEPTH)
			delTree.delegateDepth = delegateDepth;
		else
			delTree.delegateDepth = MAX_DELEGATE_DEPTH;

		return true;
	}

	// get delegation tree root status
	function getRootStatus() public constant returns (	address rootnode,
														uint delegateDepth) {
		rootnode = delTree.rootnode;
		delegateDepth = delTree.delegateDepth;
	}

	// get delegation node based on address
	function getDelToken(address id) public constant returns (	address parent,
																address[5] children,
																uint depth,
																uint delegateWidth,
																string privileges) {
		parent = delTree.nodes[id].parent;
		children = delTree.nodes[id].children;
		depth = delTree.nodes[id].depth;
		delegateWidth = delTree.nodes[id].delegateWidth;
		privileges = delTree.nodes[id].privileges;
	}

	// add new delegatee node to tree by appending to delegator's children
	function addDelToken(address delegatee) public payable returns(bool) {
		// if sender is not supervisor and sender is not in the tree
		if( supervisor != msg.sender && delTree.nodes[msg.sender].parent ==address(0) ) 
			//do nothing
			return false;

		// if delegatee in tree, do nothing to avold duplicate delegation
		if(delTree.nodes[delegatee].parent !=address(0))
			//do nothing
			return false;

		// if depth of delegator is excel maximum delegation progagation depth
		if(delTree.nodes[msg.sender].depth >= delTree.delegateDepth) 
			//do nothing
			return false;			
		
		return insertNode(msg.sender, delegatee);
	}

	// remove delegatee node from delegation tree
	function revokeDelToken(address id) public payable returns(bool) {
		// if sender is not supervisor and sender is not in the tree
		if( supervisor != msg.sender && delTree.nodes[msg.sender].parent ==address(0) ) 
			//do nothing
			return false;

		//check if revoke node is child of sender
		if(isAncestor(msg.sender, id) == false)
			//do nothing
			return false;
			
		return removeNode(id);
	}

	// update prililege data in delegatee node, support RBAC, ABAC and CapAC models 
	function setDelegateWidth(address id, uint delegateWidth) public payable returns(bool) {
		// super can set any node.
		if(supervisor == msg.sender) {
			if(delegateWidth >= MAX_DELEGATE_WIDTH)
				delTree.nodes[id].delegateWidth = MAX_DELEGATE_WIDTH;
			else
				delTree.nodes[id].delegateWidth = delegateWidth;
		}
		else {
			// node is not offspring of sender, do nothing.
			if(isAncestor(msg.sender, id) == false)
				return false;

			//get parent node
			address parent = delTree.nodes[id].parent;

			// limit that delegateWidth is so no more than parent's delegateWidth
			if( delegateWidth >= delTree.nodes[parent].delegateWidth )
				delTree.nodes[id].delegateWidth = delTree.nodes[parent].delegateWidth;
			else
				delTree.nodes[id].delegateWidth = delegateWidth;
		}
		return true;
	}

	// update prililege data in delegatee node, support RBAC, ABAC and CapAC models 
	function setPrivilege(address id, string privileges) public payable returns(bool) {
		// super can set any node.
		if(supervisor == msg.sender) {
			delTree.nodes[id].privileges = privileges;
		}
		else {
			// node is not child of sender, do nothing.
			if(isAncestor(msg.sender, id) == false)
				return false;

			delTree.nodes[id].privileges = privileges;
		}
		return true;
	}

}
