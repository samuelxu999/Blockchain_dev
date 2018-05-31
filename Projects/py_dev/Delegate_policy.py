#!/usr/bin/env python3.5

'''
========================
Delegate_Policy module
========================
Created on Apr.17, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide Delegate token struct model and encapsulation of delegation policy.
'''

import time
import datetime
import json
import sys
from web3 import Web3, HTTPProvider, IPCProvider
from Delegate_Token import DelegateToken
from utilities import DatetimeUtil, TypesUtil, FileUtil

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")

#global variable
http_provider = 'http://localhost:8042'
contract_addr = '0xbbc8eb18b19fce1457c14953e52bbc7b5f2fad3f'
contract_config = '../CapbilityToken/build/contracts/DelegateToken.json'
supervisor = '0x3d40FAD73C91AED74FfBC1F09f4cde7ccE533671'
address_zero = '0x0000000000000000000000000000000000000000'

full_delegateAR = [	'initCapToken', 
					'setCapToken_isValid', 
					'setCapToken_expireddate', 
					'setCapToken_delegateDepth', 
					'setCapToken_delegatee',
					'setCapToken_revokeDelegate',
					'setCapToken_authorization']

#new CapACToken object
mytoken=DelegateToken(http_provider, contract_addr, contract_config)
web3 = Web3(HTTPProvider(http_provider))

class DelegatePolicy(object):
	# get get_delegateTree from json data 
	@staticmethod
	def get_delegateToken(accountAddr):
		json_token={}
		root_status = mytoken.getRootStatus();
		json_token['root_node'] = root_status[0]
		json_token['max_depth'] = root_status[1]

		delToken = mytoken.getDelToken(accountAddr)
		#print(delToken)
		json_token['parent'] = delToken[0]
		json_token['children'] = delToken[1]
		json_token['depth'] = delToken[2]
		json_token['max_width'] = delToken[3]
		json_token['privilege'] = delToken[4]

		json_IDC = {}
		json_IDC['identity'] = accountAddr
		json_IDC['certificate'] = json_token
		return json_IDC

	# calculate children nodes count
	@staticmethod
	def get_childrenCount(ls_children):
		childrencount = 0
		for children in ls_children:
			if(children != address_zero):
				childrencount+=1
		return childrencount

	# delegation authorization
	@staticmethod
	def authorize_delegate(delegateeAddr, delegate_ar=[], deleWidth = 1):
		# get current node address
		BaseAddr = web3.eth.coinbase

		# get IDC for smart contract
		IDC_delegator = DelegatePolicy.get_delegateToken(BaseAddr)
		IDC_delegatee = DelegatePolicy.get_delegateToken(delegateeAddr)
		print(IDC_delegator)
		print(IDC_delegatee)

		# extract certificate from IDC
		json_delegator  = IDC_delegator['certificate']
		json_delegatee = IDC_delegatee['certificate']
		authorize_ar = ""

		# --------------------------------- delegation process --------------------------------
		#1) if delegatee node is root node(supervisor), do not delegate anymore
		if(delegateeAddr == json_delegator['root_node']):
			print("Delegatee node %s is supervisor which is not allowed to be delegated!" %(IDC_delegatee['identity']))
			return False

		#2) if delegatee node has been delegated, do not delegate anymore
		if(json_delegatee['parent']!=address_zero):
			print("Delegatee node %s has been delegated by %s!" %(json_delegatee['parent'], json_delegator['parent']))
			return False

		#3) check if children node of delegator is full
		if(DelegatePolicy.get_childrenCount(json_delegator['children'])>=json_delegator['max_width']):
			print("Chindren count of delegator has approached max_width, delegation is not allowed!")
			return False

		#4) check if delegator depth is excel max_depth
		if(json_delegator['depth']>=json_delegator['max_depth']):
			print("delegator depth has approached max_depth, delegation is not allowed!")
			return False

		#5) Verify delegated permissions
		#A) Delegator node is supervisor
		if(BaseAddr==json_delegator['root_node']):
			#authorize delegated access right			
			for ar in delegate_ar:
				#only subset of full AR is allowed to delegate
				if(ar in full_delegateAR):
					#authorize_ar.append(ar)
					authorize_ar += (ar + ';')
		
		#B) Delegator node is not supervisor
		else:						
			delgator_ar=json_delegator['privilege'].split(';')
			
			# for each delegate access right list
			for ar in delegate_ar:
				# only subset of delegator's AR is allowed to delegate
				if(ar in delgator_ar):
					#authorize_ar.append(ar)
					authorize_ar += (ar + ';')
		
		# no valid access is allowed to delegate
		if(authorize_ar==''):
			print("No access right is allow to be delegated!")
			return False	

		#6) set privilege
		print("Authorize delegation!")
		mytoken.addDelToken(delegateeAddr)
		mytoken.setDelegateWidth(delegateeAddr, deleWidth)
		mytoken.setPrivilege(delegateeAddr, authorize_ar)
		#print(authorize_ar)

		return True
	
	# check if current node is ancestor of delegatee node
	@staticmethod
	def isAncestor(ancestorAddr, delegateeAddr):
		# get current node address
		BaseAddr = web3.eth.coinbase

		# get IDC from smart contract
		IDC_delegate = DelegatePolicy.get_delegateToken(delegateeAddr)

		# extract certificate from IDC
		json_delegate = IDC_delegate['certificate']
		depth = json_delegate['depth']
		parent = json_delegate['parent']

		# find ancestor in delegate path
		curr_depth = 0
		while(curr_depth < depth):
			if(ancestorAddr == parent):
				# find ancestor in delegate path
				return True
			# search ancestor in parent node

			# get IDC from smart contract
			IDC_delegate = DelegatePolicy.get_delegateToken(parent)
			# extract certificate from IDC
			json_delegate = son_delegate = IDC_delegate['certificate']
			parent = json_delegate['parent']
			curr_depth += 1

		return False

	# delegation revocation
	@staticmethod
	def revoke_delegate(delegateeAddr):
		BaseAddr = web3.eth.coinbase
		IDC_delegatee = DelegatePolicy.get_delegateToken(delegateeAddr)
		print(IDC_delegatee)

		json_delegatee = IDC_delegatee['certificate']

		#1) current node is supervisor/root node.
		if(BaseAddr==json_delegatee['root_node']):
			if(delegateeAddr == BaseAddr):
				print("Root node is not allow to revoke!")
				return False
			else:
				print("Revoke by root node!")
				mytoken.revokeDelToken(delegateeAddr)
		else:
			# Not delegated node, skip reviocation
			if(json_delegatee['parent']==address_zero):
				print("Current node is not delegated, do nothing!")
				return False

			if( (BaseAddr != delegateeAddr) and 
				(DelegatePolicy.isAncestor(BaseAddr, delegateeAddr) == False) ):
				print("Neither supervisor nor ancestor, revocation is not allowed!")
				return False

			print("Revoke by ancestor node!")
			mytoken.revokeDelToken(delegateeAddr)

		return True
		


if __name__ == "__main__":

	#Get account address
	rootAddr = '0x3d40FAD73C91AED74FfBC1F09f4cde7ccE533671'
	accountAddr = '0x6bf852ca042667d7676248a5d1429142137d12d4'
	accountAddr1 = '0xaf81309bc2a3bdbfca8576120e96fb34d8cd12e7'
	accountAddr2 = '0xa8bbb9f68da15e09e9d09100d38031a46d0581cd'
	accountAddr3 = '0xf30db537acb08b46084af8ca8083befe524aaf30'
	accountAddr4 = '0xaa09c6d65908e54bf695748812c51d8f2ceea0f5'
	accountAddr5 = '0xfa4c5d320d638cbdff557c4c1f3110d3143f40c3'
	accountAddr6 = '0x781008570ef49283518c09007092b8341c5d040a'

	delegate_data = DelegatePolicy.get_delegateToken(accountAddr4)
	print(delegate_data)

	ls_delegateAR=['initCapToken', 
					'setCapToken_isValid',
					'setCapToken_revokeDelegate']

	#print(DelegatePolicy.authorize_delegate(accountAddr4, ls_delegateAR, 1))

	#print(DelegatePolicy.revoke_delegate(accountAddr4))

	pass