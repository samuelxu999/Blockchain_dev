pragma solidity ^0.4.18;

contract DelegateToken {

	/*
		Define struct to represent delegation node data.
	*/
	struct Node {
		address parent;				// delegatee address
		address[5] children;		// children nodes, maximum delegation width is 5
		uint depth;					// current node depth
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

	/************************************* tree functions ******************************************/
	function insertNode(address delegator, address delegatee, string privileges) 
			private returns (bool) {
		// DelegateTree is not initialized
		if(delTree.rootnode == address(0)) 
			return false;
		
		// check whether delegator is existed in delTree
		if( (delTree.rootnode != delegator) && (delTree.nodes[delegator].parent == address(0)) ) {
			return false;
		}

		//get children length
		uint children_length = delTree.nodes[delegator].children.length;
		uint empty_slot = children_length;

		// check children nodes
		for(uint i = 0; i < children_length; i++) {
			// node has already in the delTree
			if(delTree.nodes[delegator].children[i] == delegatee) {
				return false;
			}

			//find empty slot
			if(delTree.nodes[delegator].children[i] == address(0)) {
				empty_slot = i;
			}
		}

		//check whether children nodes are full
		if(empty_slot >= children_length) {
			return false;
		}

		// add new delegatee address to children
		delTree.nodes[delegator].children[empty_slot] = delegatee;
		
		// update node based on delegatee address
		delTree.nodes[delegatee].parent = delegator;
		delTree.nodes[delegatee].depth = delTree.nodes[delegator].depth + 1;
		delTree.nodes[delegatee].privileges = privileges;

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

		// get children length
		uint children_length = delTree.nodes[parent].children.length;
		uint i;

		// remove node from parent's children list
		for(i = 0; i < children_length; i++) { 
			if(delTree.nodes[parent].children[i] == id) {
				delTree.nodes[parent].children[i] = address(0);
				break;
			}
		}

		// clear current node data
		delTree.nodes[id].parent = address(0);
		delTree.nodes[id].depth = 0;
		delTree.nodes[id].privileges = '';

		// delete children node
		children_length = delTree.nodes[id].children.length;
		for(i = 0; i < children_length; i++) { 
			if(delTree.nodes[id].children[i] == address(0)) 
				continue;

			//delete child
			removeNode(delTree.nodes[id].children[i]);
		}

		return true;
	}


	// Global state variables
	address private constant supervisor = 0x3d40fad73c91aed74ffbc1f09f4cde7cce533671;
	Tree private delTree;

	/************************************* transaction function ******************************************/
	function initTree() public payable returns(bool) {
		if( supervisor != msg.sender) 
			return false;
		// initialize tree
		delTree.rootnode = supervisor;
		delTree.delegateDepth = 1;
		// initialize rootnode
		delTree.nodes[supervisor].parent = address(0);
		delTree.nodes[supervisor].depth = 0;
		delTree.nodes[supervisor].privileges = 'suporvisor';
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
																string privileges) {
		parent = delTree.nodes[id].parent;
		children = delTree.nodes[id].children;
		depth = delTree.nodes[id].depth;
		privileges = delTree.nodes[id].privileges;
	}

	// add new delegatee node to tree by appending to delegator's children
	function addDelToken(address delegatee, string privileges) public payable returns(bool) {
		return insertNode(msg.sender, delegatee, privileges);
	}

	// remove delegatee node from delegation tree
	function revokeDelToken(address id) public payable returns(bool) {
		return removeNode(id);
	}

	// update prililege data in delegatee node, support RBAC, ABAC and CapAC models 
	function setPrivilege(address id, string privileges) public payable returns(bool) {
		delTree.nodes[id].privileges = privileges;
		return true;
	}

}
