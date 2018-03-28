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

class ABACToken(object):
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
	def getAttributeToken(self, account_addr):
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
		role = self.contract.call({'from': self.web3.eth.coinbase}).getAttribute(checksumAddr)
		token_data.append(role)
		return token_data

	#initialized token by sending transact to call initRoleToken()
	def initAttributeToken(self, account_addr):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(account_addr)

		# Execute the specified function by sending a new public transaction.
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).initAttributeToken(checksumAddr)

	# set isValid flag in token
	def setAttributeToken_isValid(self, recipient, flag_value):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setAttributeToken_isValid(checksumAddr, flag_value)

	# set issue date and expired date
	def setAttributeToken_expireddate(self, recipient, issue_time, expire_time):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setAttributeToken_expireddate(checksumAddr, issue_time, expire_time)

	# set delegation depth
	def setAttributeToken_delegateDepth(self, recipient, depth):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setAttributeToken_delegateDepth(checksumAddr, depth)

	# set delegatee
	def setAttributeToken_delegatee(self, recipient, delegatee):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(recipient)	
		checksum_delegatee = Web3.toChecksumAddress(delegatee)

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setAttributeToken_delegatee(checksumAddr, checksum_delegatee)

	# revoke delegatee
	def setAttributeToken_revokeDelegate(self, recipient, delegatee):
		#Change account address to EIP checksum format
		checksumAddr = Web3.toChecksumAddress(recipient)	
		checksum_delegatee = Web3.toChecksumAddress(delegatee)

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setAttributeToken_revokeDelegate(checksumAddr, checksum_delegatee)

	# set issue date and expired date
	def setAttributeToken_Attribute(self, recipient, role):
		#Change account address to EIP checksum format
		checksumAddr=Web3.toChecksumAddress(recipient)	

		# Execute the specified function by sending a new public transaction.	
		ret=self.contract.transact({'from': self.web3.eth.coinbase}).setAttributeToken_Attribute(checksumAddr, role)

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

def generateAttribute():
	attribute_json={}

	#construct user attribute
	attribute_user=[]
	attribute_user.append('admin')
	attribute_user.append('viewer')
	attribute_json['attrUser']=attribute_user

	#construct action attribute
	attribute_action=[]
	attribute_action.append('Get')
	attribute_action.append('Post')
	attribute_json['attrAction']=attribute_action

	#construct resource attribute
	attribute_resource=[]
	attribute_resource.append('/test/api/v1.0/dt')
	attribute_resource.append('/test/api/v1.0/dt/project')
	attribute_json['attrResource']=attribute_resource

	#construct envrionmental attribute
	attribute_environment=[]

	#define environmental attribute
	env_time={}
	env_time['type']='Timespan'
	env_time['value']={}
	env_time['value']['start']='8:12:32'
	env_time['value']['end']='14:12:32'
	attribute_environment.append(env_time)

	env_location={}
	env_location['type']='Location'
	env_location['value']={}
	env_location['value']['GPS']='11, 23l, 18'
	env_location['value']['Area']='120'
	attribute_environment.append(env_location)

	attribute_json['attrEnvironment']=attribute_environment

	return attribute_json


if __name__ == "__main__":
	http_provider = 'http://localhost:8042'
	contract_addr = '0xc5c2e2e98fcdaaa0c567d2cbd7be7e7206bcf4dd'
	contract_config = '../CapbilityToken/build/contracts/ABACToken.json'

	#Get account address
	accountAddr=ABACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')
	print("Account: " + accountAddr)
	#new ABACToken object
	mytoken=ABACToken(http_provider, contract_addr, contract_config)
	#mytoken.Show_ContractInfo()


	#------------------------- test contract API ---------------------------------
	#getAccounts
	accounts = mytoken.getAccounts()
	balance = mytoken.getBalance('0x950d8eb4825c597534027638c862496ea0d7cf43')
	print(accounts)
	print(balance)

	#Read token data using call
	token_data=mytoken.getAttributeToken(accountAddr);
	ABACToken.print_tokendata(token_data)
	
	# list Access control
	'''json_data=TypesUtil.string_to_json(token_data[-1][1])
	print(json_data['resource'])
	print(json_data['action'])
	print(json_data['conditions'])'''

	#Send transact
	#mytoken.initAttributeToken(accountAddr);
	#mytoken.setAttributeToken_isValid(accountAddr, True)

	#set issue date and expired date
	nowtime = datetime.datetime.now()
	#calculate issue_time and expire_time
	issue_time = DatetimeUtil.datetime_timestamp(nowtime)
	duration = DatetimeUtil.datetime_duration(0, 1, 0, 0)
	expire_time = DatetimeUtil.datetime_timestamp(nowtime + duration)
	#mytoken.setAttributeToken_expireddate(accountAddr, issue_time, expire_time)

	#set delegation right
	#mytoken.setAttributeToken_delegateDepth(accountAddr, 4)
	#mytoken.setAttributeToken_delegatee(accountAddr, '0x9c2da23272c8fec791c54febd0507fb519730cee')
	#mytoken.setAttributeToken_revokeDelegate(accountAddr, '0x9c2da23272c8fec791c54febd0507fb519730cee')

	#set attribute
	attribute=generateAttribute();
	str_attribute=TypesUtil.json_to_string(attribute)
	#mytoken.setAttributeToken_Attribute(accountAddr, str_attribute)

	#read attribute
	'''read_attr=TypesUtil.string_to_json(token_data[2][1])
	print(read_attr['attrEnvironment'][1]['value'])'''

	pass