#!/usr/bin/env python3.5

'''
========================
Capability token module
========================
Created on Mar.8, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with smart contract.
'''

from web3 import Web3, HTTPProvider, IPCProvider
from utilities import DatetimeUtil, TypesUtil
import json, datetime, time

class CapACToken(object):
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

	#get token data by call getCapToken()
	def getCapToken(self, account_addr):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(account_addr)

		token_data = []
		'''
		Call a contract function, executing the transaction locally using the eth_call API. 
		This will not create a new public transaction.
		'''

		# get token status
		tokenStatus=self.contract.call({'from': self.web3.eth.coinbase}).getCapTokenStatus(checksumAddr)
		token_data.append(tokenStatus)

		# get delegate status
		deelgateStatus = self.contract.call({'from': self.web3.eth.coinbase}).getDelegateStatus(checksumAddr)
		token_data.append(deelgateStatus)

		# get authorization data
		authorization = self.contract.call({'from': self.web3.eth.coinbase}).getAuthorization(checksumAddr)
		token_data.append(authorization)
		return token_data

	#initialized token by sending transact to call initCapToken()
	def initCapToken(self, account_addr):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).initCapToken(checksumAddr)

	# set isValid flag in token
	def setCapToken_isValid(self, recipient, flag_value):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setCapToken_isValid(checksumAddr, flag_value)

	# set issue date and expired date
	def setCapToken_expireddate(self, recipient, issue_time, expire_time):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setCapToken_expireddate(checksumAddr, issue_time, expire_time)

	# set delegation depth
	def setCapToken_delegateDepth(self, recipient, depth):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setCapToken_delegateDepth(checksumAddr, depth)

	# set delegatee
	def setCapToken_delegatee(self, recipient, delegatee):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(recipient)	
		checksum_delegatee = Web3.toChecksumAddress(delegatee)

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setCapToken_delegatee(checksumAddr, checksum_delegatee)

	# revoke delegatee
	def setCapToken_revokeDelegate(self, recipient, delegatee):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(recipient)	
		checksum_delegatee = Web3.toChecksumAddress(delegatee)

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setCapToken_revokeDelegate(checksumAddr, checksum_delegatee)

	# set issue date and expired date
	def setCapToken_authorization(self, recipient, access_right):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setCapToken_authorization(checksumAddr, access_right)

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
	contract_addr = '0x23cd84b2dfc81a5feb312d1a7217d6537b90d2f8'
	contract_config = '../CapbilityToken/build/contracts/CapACToken.json'

	#Get account address
	accountAddr=CapACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')
	print("Account: " + accountAddr)
	#new CapACToken object
	mytoken=CapACToken(http_provider, contract_addr, contract_config)
	#mytoken.Show_ContractInfo()


	#------------------------- test contract API ---------------------------------
	#getAccounts
	accounts = mytoken.getAccounts()
	balance = mytoken.getBalance('0x950d8eb4825c597534027638c862496ea0d7cf43')
	print(accounts)
	print(balance)

	#Read token data using call
	token_data=mytoken.getCapToken(accountAddr);
	CapACToken.print_tokendata(token_data)
	
	# list Access control
	'''json_data=TypesUtil.string_to_json(token_data[-1][1])
	print(json_data['resource'])
	print(json_data['action'])
	print(json_data['conditions'])'''

	#Send transact
	#mytoken.initCapToken(accountAddr);
	#mytoken.setCapToken_isValid(accountAddr, True)

	#set issue date and expired date
	nowtime = datetime.datetime.now()
	#calculate issue_time and expire_time
	issue_time = DatetimeUtil.datetime_timestamp(nowtime)
	duration = DatetimeUtil.datetime_duration(0, 1, 0, 0)
	expire_time = DatetimeUtil.datetime_timestamp(nowtime + duration)
	#mytoken.setCapToken_expireddate(accountAddr, issue_time, expire_time)

	#set delegation right
	#mytoken.setCapToken_delegateDepth(accountAddr, 3)
	#mytoken.setCapToken_delegatee(accountAddr, '0x9c2da23272c8fec791c54febd0507fb519730cee')
	#mytoken.setCapToken_revokeDelegate(accountAddr, '0x9c2da23272c8fec791c54febd0507fb519730cee')

	#set access right
	access_right='{"resource":"/test/api/v1.0/dt", "action":"GET", "conditions":{"value": {"start": "8:12:32", "end": "14:32:32"},"type": "Timespan"}}';
	#mytoken.setCapToken_authorization(accountAddr, access_right)

	pass