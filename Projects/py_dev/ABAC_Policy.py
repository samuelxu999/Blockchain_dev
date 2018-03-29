#!/usr/bin/env python3.5

'''
========================
ABAC_Policy module
========================
Created on Mar.28, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide Attribute based AC token struct model and encapsulation of access control policy.
'''

import time
import datetime
import json
import sys
from ABAC_Token import ABACToken
from utilities import DatetimeUtil, TypesUtil, FileUtil
from db_layer import ABACRuleManager
from flask import request

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")

#global variable
http_provider = 'http://localhost:8042'
contract_addr = '0xc5c2e2e98fcdaaa0c567d2cbd7be7e7206bcf4dd'
contract_config = '../CapbilityToken/build/contracts/ABACToken.json'
path_db='ABAC.db'

#new ABACToken object
mytoken=ABACToken(http_provider, contract_addr, contract_config)

'''
Capability access control policy management
'''
class ABACPolicy(object):

	# get token data from smart contract, return json fromat
	@staticmethod
	def get_token(accountAddr):
		token_data=mytoken.getAttributeToken(accountAddr);
		json_token={}

		#Add status information
		tokenStatus = token_data[0]
		json_token['id'] = tokenStatus[0]
		json_token['initialized'] = tokenStatus[1]
		json_token['isValid'] = tokenStatus[2]
		json_token['issuedate'] = tokenStatus[3]
		json_token['expireddate'] = tokenStatus[4]

		#Add delegation information
		tokenDelegation = token_data[1]
		json_token['delegateDepth'] = tokenDelegation[0]
		json_token['delegatee'] = tokenDelegation[1]

		#Add authorization information
		tokenRole = token_data[2]
		json_token['attribute'] = tokenRole[1]

		return json_token

	# check token status, like status flag, issue and expire time.
	@staticmethod
	def is_token_valid(token_data):
		ret = True
		#check enable flag
		if( token_data['initialized']!=True or token_data['isValid']!=True):
			ret = False

		#check issue time and expire time
		now_stamp = DatetimeUtil.datetime_timestamp(datetime.datetime.now())
		if( (token_data['issuedate'] > now_stamp) or (now_stamp > token_data['expireddate']) ):
			ret = False
		return ret

	# verify acccess right
	@staticmethod
	def is_access_valid(token_data, acess_args=''):
		ret = False
		#print(token_data)
		#query access right associated to role from local database
		#rule_entry=ABACRuleManager.select_ByName(path_db, 'rule2')
		#print(rule_entry)

		#Find rule associated to resource
		field_data = {}
		field_data['AttrResource'] = str(acess_args['url_rule'])
		rules_entry = ABACRuleManager.select_ByFieldname(path_db, field_data)

		if(len(rules_entry)>0):		
			#print(rules_entry)

			token_attribute = TypesUtil.string_to_json(token_data['attribute'])
			#print(token_attribute['attrUser'][0])
			#print(token_attribute)
			for rule_entry in rules_entry: 
				json_env=TypesUtil.string_to_json(rule_entry['AttrEnvironment'])
				#print(json_env['value'])

				if(rule_entry['AttrUser'] in token_attribute['attrUser'] and
					acess_args['method'] in token_attribute['attrAction'] and 
					str(acess_args['url_rule']) in token_attribute['attrResource'] and
					ABACPolicy.is_condition_valid(json_env)):
					#print(token_attribute[''])
					ret = True
					break

				'''print(rule_entry['AttrUser'] in token_attribute['attrUser'])
				print(acess_args['method'] in token_attribute['attrAction'])
				print(str(acess_args['url_rule']) in token_attribute['attrResource'])
				print(ABACPolicy.is_condition_valid(json_env))'''

		return ret

	# check condition status to verify context requirement
	@staticmethod
	def is_condition_valid(condition_data):
		if(condition_data==[]):
			return True
		#handle Timespan
		if(condition_data['type']=='Timespan'):
			#print condition_data['value']['start']
			starttime = DatetimeUtil.string_datetime(condition_data['value']['start'], "%H:%M:%S")
			endtime = DatetimeUtil.string_datetime(condition_data['value']['end'], "%H:%M:%S")
			nowtime=DatetimeUtil.string_datetime(timestr, "%H:%M:%S")
			'''print(starttime)
			print(endtime)
			print(nowtime)'''
			#check if timespan condition is valid
			if(not (starttime<nowtime<endtime) ):
				print("condition validation fail!")
				return False
		return True

	'''
	Valid access request based on policy, call by interposing service API
	'''	
	@staticmethod	
	def is_valid_access_request(req_args):
		#Get account address
		accountAddr=ABACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')

		#Define ls_time_exec to save executing time to log
		ls_time_exec=[]

		#get token data
		start_time=time.time()

		# 1) get token from smart contract, high overload
		token_data=ABACPolicy.get_token(accountAddr)

		# 2) Save token data to local token.dat
		#FileUtil.AddLine('ABAC_token.dat', TypesUtil.json_to_string(token_data))

		# 3) read token from local data, low overload
		'''read_token=FileUtil.ReadLines('ABAC_token.dat')
		token_data=TypesUtil.string_to_json(read_token[0])'''
		#print(token_data)

		exec_time=time.time()-start_time
		ls_time_exec.append(format(exec_time*1000, '.3f'))	
		print("Execution time of get_token is:%2.6f" %(exec_time))

		#extract access action from request
		access_data={}
		access_data['url_rule']=req_args.url_rule
		access_data['method']=req_args.method
		#print(access_data)

		start_time=time.time()
		if(not ABACPolicy.is_token_valid(token_data)):
			print('token valid fail')
			return False
		exec_time=time.time()-start_time
		ls_time_exec.append(format(exec_time*1000, '.3f'))	
		print("Execution time of is_token_valid is:%2.6f" %(exec_time))

		start_time=time.time()
		if(not ABACPolicy.is_access_valid(token_data, access_data)):
			print('access valid fail')
			return False
		exec_time=time.time()-start_time
		ls_time_exec.append(format(exec_time*1000, '.3f'))		
		print("Execution time of is_access_valid is:%2.6f" %(exec_time))

		#transfer list to string
		str_time_exec=" ".join(ls_time_exec)
		#print(str_time_exec)
		FileUtil.AddLine('exec_time_server.log', str_time_exec)

		return True

def test_CapACToken():


	#Get account address
	accountAddr=ABACToken.getAddress('sam_miner_win7_0', '../CapbilityToken/test/addr_list.json')
	#print("Account: " + accountAddr)

	#Read token data using call
	token_data=mytoken.getAttributeToken(accountAddr);
	ABACToken.print_tokendata(token_data)
	#print(token_data)


	'''token_data=ABACPolicy.get_token(accountAddr)
	print(token_data['delegatee'][0])
	attr_data = TypesUtil.string_to_json(token_data['attribute'])
	print(attr_data['attrEnvironment'][1]['value'])'''

	#FileUtil.AddLine('token.dat', TypesUtil.json_to_string(token_data))

	'''read_token=FileUtil.ReadLines('token.dat')
	json_token=TypesUtil.string_to_json(read_token[0])
	print(json_token['initialized'])'''

	#ret=RBACPolicy.is_token_valid(token_data)

	#ret=ABACPolicy.is_access_valid(token_data)
	#print(ret)
	

if __name__ == "__main__":

	test_CapACToken()
	pass
