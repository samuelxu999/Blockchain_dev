#!/usr/bin/env python3.5

'''
========================
Delegate token module
========================
Created on Apr.15, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with smart contract.
'''

from web3 import Web3, HTTPProvider, IPCProvider
from utilities import DatetimeUtil, TypesUtil
import json, datetime, time

class DelegateToken(object):
	def __init__(self, http_provider, contract_addr, contract_config):
		# configuration initialization
		self.web3 = Web3(HTTPProvider(http_provider))
		self.contract_address=Web3.toChecksumAddress(contract_addr)
		self.contract_config = json.load(open(contract_config))

		# new contract object
		self.contract=self.web3.eth.contract()
		self.contract.address=self.contract_address
		self.contract.abi=self.contract_config['abi']

	def Show_ContractInfo(self):  
		print(self.web3.eth.blockNumber)
		print(self.web3.eth.accounts)
		print(self.web3.fromWei(self.web3.eth.getBalance(self.web3.eth.accounts[0]), 'ether'))

		print(self.contract.address)

	# return accounts address
	def getAccounts(self):
		return self.web3.eth.accounts

	# return accounts balance
	def getBalance(self, account_addr=''):
		if(account_addr==''):
			# get accounts[0] balance
			checksumAddr=self.web3.eth.coinbase
		else:
			#Change account address to EIP checksum format
			checksumAddr=Web3.toChecksumAddress(account_addr)	
		return self.web3.fromWei(self.web3.eth.getBalance(checksumAddr), 'ether')

	#get token data
	def getRootStatus(self):
		# get token status
		rootStatus=self.contract.call({'from': self.web3.eth.coinbase}).getRootStatus()

		return rootStatus

	#get token data
	def getDelToken(self, account_addr):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(account_addr)

		# get token data
		token_data=self.contract.call({'from': self.web3.eth.coinbase}).getDelToken(checksumAddr)

		return token_data

	# Print token date
	@staticmethod
	def print_tokendata(token_data):
		#print token status
		for i in range(0,len(token_data)):
			print(token_data[i])

	# get address from json file
	@staticmethod
	def getAddress(node_name, datafile):
		address_json = json.load(open(datafile))
		return address_json[node_name]

	#initialized token by sending transact to call initCapToken()
	def initDelegateTree(self):
		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).initTree()

	# set delegateDepth to call setTreeDepth()
	def setDelegateDepth(self, delegateDepth):
		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setTreeDepth(delegateDepth)

	#add token by sending transact to call addDelToken()
	def addDelToken(self, account_addr):
		#Change account address to EIP checksum format
		delegatee = Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).addDelToken(delegatee)

	# revoke delegatee by sending transact to call revokeDelToken()
	def revokeDelToken(self, account_addr):
		#Change account address to EIP checksum format
		delegatee = Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).revokeDelToken(delegatee)

	# update privilege in node by sending transact to call setPrivilege()
	def setPrivilege(self, account_addr, privilege):
		#Change account address to EIP checksum format
		delegatee = Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setPrivilege(delegatee, privilege)

	# update delegateWidth of node by sending transact to call setDelegateWidth()
	def setDelegateWidth(self, account_addr, delegateWidth):
		#Change account address to EIP checksum format
		delegatee = Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setDelegateWidth(delegatee, delegateWidth)


if __name__ == "__main__":
	http_provider = 'http://localhost:8042'
	contract_addr = '0xbbc8eb18b19fce1457c14953e52bbc7b5f2fad3f'
	contract_config = '../CapbilityToken/build/contracts/DelegateToken.json'

	#Get account address
	accountAddr=DelegateToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')
	print("Account: " + accountAddr)
	#new CapACToken object
	mytoken=DelegateToken(http_provider, contract_addr, contract_config)
	#mytoken.Show_ContractInfo()


	#------------------------- test contract API ---------------------------------
	#getAccounts
	accounts = mytoken.getAccounts()
	balance = mytoken.getBalance('0x950d8eb4825c597534027638c862496ea0d7cf43')
	print(accounts)
	print(balance)

	#Get account address
	accountAddr='0x6bf852ca042667d7676248a5d1429142137d12d4'

	accountAddr1='0xaf81309bc2a3bdbfca8576120e96fb34d8cd12e7'
	accountAddr2='0xa8bbb9f68da15e09e9d09100d38031a46d0581cd'
	accountAddr3='0xf30db537acb08b46084af8ca8083befe524aaf30'
	accountAddr4='0xaa09c6d65908e54bf695748812c51d8f2ceea0f5'
	accountAddr5='0xfa4c5d320d638cbdff557c4c1f3110d3143f40c3'
	accountAddr6='0x781008570ef49283518c09007092b8341c5d040a'

	#Read token data using call
	token_status = mytoken.getRootStatus();
	print(token_status)
	root_node=mytoken.getDelToken(token_status[0]);
	DelegateToken.print_tokendata(root_node)
	token_data=mytoken.getDelToken(accountAddr);
	DelegateToken.print_tokendata(token_data)
	
	# list Access control
	'''json_data=TypesUtil.string_to_json(token_data[-1][1])
	print(json_data['resource'])
	print(json_data['action'])
	print(json_data['conditions'])'''

	#Send transact
	#mytoken.initDelegateTree()
	#mytoken.setDelegateDepth(6)
	#mytoken.addDelToken(accountAddr0)
	#mytoken.setPrivilege(accountAddr, 'update delegatee')
	#mytoken.setDelegateWidth(accountAddr, 6)
	#mytoken.revokeDelToken(accountAddr4)

	pass