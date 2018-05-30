#!/usr/bin/env python3.5

from web3 import Web3, HTTPProvider, IPCProvider
import json
from utilities import DatetimeUtil, TypesUtil

web3 = Web3(HTTPProvider('http://localhost:8042'))

#web3 = Web3(IPCProvider())

class BCPerformance(object):
	# get current block number 
	@staticmethod
	def getBlocknumber():
		print("Current block number is: %d" %(web3.eth.blockNumber)) 

	# get current account information
	@staticmethod
	def getAccounts():
		print("Current accounts on this machine are:")
		for account in web3.eth.accounts:
			print("--- Address: %s  Balance: %s" %(account, web3.fromWei(web3.eth.getBalance(account), 'ether')))

	# calculate average block generate time 
	@staticmethod
	def calculate_blocktime(block_number, curr_blkNum=0):
		#get current block number to search back
		if(curr_blkNum ==0):
			blk_number=web3.eth.blockNumber
		else:
			blk_number = curr_blkNum

		sum_time=0
		skip_count=0
		for i in range(0, block_number-1):
			blk=web3.eth.getBlock(blk_number-i)
			dt=DatetimeUtil.timestamp_datetime(blk.timestamp*1000)
			#print(DatetimeUtil.datetime_string(dt))
			time_diff=web3.eth.getBlock(blk_number-i).timestamp-web3.eth.getBlock(blk_number-i-1).timestamp
			if(time_diff>60):
				skip_count+=1
			else:
				sum_time+=time_diff
			#print(time_diff)
		#print(skip_count)
		ave_blocktime=sum_time/(block_number-skip_count)
		return ave_blocktime

	# calculate average gas used for transactions 
	@staticmethod
	def calculate_transactionGas(block_count, curr_blkNum=0):
		#get current block number to search back
		if(curr_blkNum ==0):
			blk_number=web3.eth.blockNumber
		else:
			blk_number = curr_blkNum

		sum_gas=0
		trans_count = 0
		for i in range(0, block_count-1):
			blk=web3.eth.getBlock(blk_number-i)
			if(blk.transactions!=[]):
				for trans in blk.transactions:
					#print(web3.eth.getTransaction(trans))
					sum_gas+=web3.eth.getTransaction(trans).gas
					trans_count+=1
			#print(time_diff)
		print(trans_count)
		ave_gas=sum_gas/trans_count
		return ave_gas


if __name__ == "__main__":

	BCPerformance.getBlocknumber()
	BCPerformance.getAccounts()
	#print(web3.eth.getTransaction('0xbd358846c24c421056d86af0d042ec1a59a97be40b485acc2c3e209c5a6785e3'))
	print("2 miners: %.2f" %(BCPerformance.calculate_blocktime(60, 41765)))
	print("3 miners: %.2f" %(BCPerformance.calculate_blocktime(60, 41825)))
	print("4 miners: %.2f" %(BCPerformance.calculate_blocktime(60, 41885)))
	print("5 miners: %.2f" %(BCPerformance.calculate_blocktime(60, 41945)))
	print("6 miners: %.2f" %(BCPerformance.calculate_blocktime(60, 42010)))
	print("7 miners: %.2f" %(BCPerformance.calculate_blocktime(60, 42150)))
	print("Average gas for transaction: %.2f" %(BCPerformance.calculate_transactionGas(1000)))
	pass