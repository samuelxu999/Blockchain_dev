#!/usr/bin/env python3.5

'''
========================
RBAC token module
========================
Created on Mar.26, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with smart contract.
'''

from web3 import Web3, HTTPProvider, IPCProvider
from utilities import DatetimeUtil, TypesUtil
import json, datetime, time

class RBACToken(object):
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

	#get token data by call getTokenStatus()
	def getRoleToken(self, account_addr):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(account_addr)

		token_data = []
		'''
		Call a contract function, executing the transaction locally using the eth_call API. 
		This will not create a new public transaction.
		'''

		# get token status
		tokenStatus=self.contract.call({'from': self.web3.eth.coinbase}).getTokenStatus(checksumAddr)
		token_data.append(tokenStatus)

		# get delegate status
		deelgateStatus = self.contract.call({'from': self.web3.eth.coinbase}).getDelegateStatus(checksumAddr)
		token_data.append(deelgateStatus)

		# get role data
		role = self.contract.call({'from': self.web3.eth.coinbase}).getRole(checksumAddr)
		token_data.append(role)
		return token_data

	#initialized token by sending transact to call initRoleToken()
	def initRoleToken(self, account_addr):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).initRoleToken(checksumAddr)

	# set isValid flag in token
	def setRoleToken_isValid(self, recipient, flag_value):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setRoleToken_isValid(checksumAddr, flag_value)

	# set issue date and expired date
	def setRoleToken_expireddate(self, recipient, issue_time, expire_time):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setRoleToken_expireddate(checksumAddr, issue_time, expire_time)

	# set delegation depth
	def setRoleToken_delegateDepth(self, recipient, depth):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setRoleToken_delegateDepth(checksumAddr, depth)

	# set delegatee
	def setRoleToken_delegatee(self, recipient, delegatee):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(recipient)	
		checksum_delegatee = Web3.toChecksumAddress(delegatee)

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setRoleToken_delegatee(checksumAddr, checksum_delegatee)

	# revoke delegatee
	def setRoleToken_revokeDelegate(self, recipient, delegatee):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(recipient)	
		checksum_delegatee = Web3.toChecksumAddress(delegatee)

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setRoleToken_revokeDelegate(checksumAddr, checksum_delegatee)

	# set issue date and expired date
	def setRoleToken_role(self, recipient, role):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setRoleToken_Role(checksumAddr, role)

	# Print token date
	@staticmethod
	def print_tokendata(token_data):
		#print token status
		for i in range(0,len(token_data[0])):
			if(i==3 or i==4):
				dt=DatetimeUtil.timestamp_datetime(token_data[0][i])
				#dt=datetime.datetime.utcfromtimestamp(token_data[i]/1e3)
				print(DatetimeUtil.datetime_string(dt))
				#print(DatetimeUtil.datetime_timestamp(dt))
				#print(token_data[i])
			else:
				print(token_data[0][i])

		#print delegation status
		for i in range(0,len(token_data[1])):
			print(token_data[1][i])


		#print authprization status
		print(token_data[2])

	# get address from json file
	@staticmethod
	def getAddress(node_name, datafile):
		address_json = json.load(open(datafile))
		return address_json[node_name]

if __name__ == "__main__":
	http_provider = 'http://localhost:8042'
	contract_addr = '0x3fa4a39c4657acc936ac1c598ff24c6e9a34b1a9'
	contract_config = '../CapbilityToken/build/contracts/RBACToken.json'

	#Get account address
	accountAddr=RBACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')
	print("Account: " + accountAddr)
	#new RBACToken object
	mytoken=RBACToken(http_provider, contract_addr, contract_config)
	#mytoken.Show_ContractInfo()


	#------------------------- test contract API ---------------------------------
	#getAccounts
	accounts = mytoken.getAccounts()
	balance = mytoken.getBalance('0x950d8eb4825c597534027638c862496ea0d7cf43')
	print(accounts)
	print(balance)

	#Read token data using call
	token_data=mytoken.getRoleToken(accountAddr);
	RBACToken.print_tokendata(token_data)
	
	# list Access control
	'''json_data=TypesUtil.string_to_json(token_data[-1][1])
	print(json_data['resource'])
	print(json_data['action'])
	print(json_data['conditions'])'''

	#Send transact
	#mytoken.initRoleToken(accountAddr);
	#mytoken.setRoleToken_isValid(accountAddr, True)

	#set issue date and expired date
	nowtime = datetime.datetime.now()
	#calculate issue_time and expire_time
	issue_time = DatetimeUtil.datetime_timestamp(nowtime)
	duration = DatetimeUtil.datetime_duration(0, 1, 0, 0)
	expire_time = DatetimeUtil.datetime_timestamp(nowtime + duration)
	#mytoken.setRoleToken_expireddate(accountAddr, issue_time, expire_time)

	#set delegation right
	#mytoken.setRoleToken_delegateDepth(accountAddr, 3)
	#mytoken.setRoleToken_delegatee(accountAddr, '0x9c2da23272c8fec791c54febd0507fb519730cee')
	#mytoken.setRoleToken_revokeDelegate(accountAddr, '0x9c2da23272c8fec791c54febd0507fb519730cee')

	#set role
	role='admin';
	#mytoken.setRoleToken_role(accountAddr, role)

	pass