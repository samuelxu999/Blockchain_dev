#!/usr/bin/env python3

'''
========================
PRC_Client module
========================
Created on Feb.9, 2020
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of basic API that access to Tendermint RPC.
'''

import requests
import json
import time
import os
from utilities import TypesUtil,FileUtil

class PRC_Client(object):

    '''
    Get abci_info:     curl -s 'localhost:26657/abci_info'
    '''
    @staticmethod
    def abci_info():
        headers = {'Content-Type' : 'application/json'}
        response = requests.get('http://localhost:26657/abci_info', headers=headers)

        # print(response.status_code)
        # print(response.headers['content-type'])
        # print(response.encoding)
        # print(response.text)
        # print(response.json())

        #get response json
        json_response = response.json()      

        return json_response
    

    '''
    Execute abci_query: curl -s 'localhost:26657/abci_query?data="abcd"'
    '''
    # @staticmethod
    def abci_query(params_json={}):            
        headers = {'Content-Type' : 'application/json'}
        api_url='http://localhost:26657/abci_query'
 
        response = requests.get(api_url, params=params_json, headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response

    '''
    Send transaction to network
    curl -s 'localhost:26657/broadcast_tx_commit?tx="sam"'
    '''
    @staticmethod
    def broadcast_tx_commit(params_json={}):          
        headers = {'Content-Type' : 'application/json'}
        api_url='http://localhost:26657/broadcast_tx_commit'

        response = requests.post(api_url, params=params_json, headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response

def test_query(tx_json):
	query_ret = PRC_Client.abci_query(tx_json)
	print(query_ret)

	key_str = query_ret['result']['response']['key']
	if(key_str != None):
	    print("key:"+TypesUtil.base64_to_ascii(key_str))

	value_str = query_ret['result']['response']['value']
	if(value_str != None):
		str_ascii = TypesUtil.base64_to_ascii(value_str)
		print("value:"+str_ascii)   

		# -------------- Display json value ------------
		# json_data = TypesUtil.tx_to_json(str_ascii) 
		# print(json_data['name'])  
		# print(json_data['age']) 

def test_tx_commit(tx_json):
    query_ret = PRC_Client.broadcast_tx_commit(tx_json)
    print(query_ret)
    pass

if __name__ == "__main__":
	#========================= test info =====================
	print(PRC_Client.abci_info())
	

	#==================== test query =========================
	query_json = {}

	# --------------------- counter ----------------------
	# tx_data = "tx"
	# tx_data = "hash"    
	# query_json['path']='"' + tx_data +'"'
	# test_query(query_json)

	# ------------------------kvstore ----------------------
	kv_mode = 0

	if(kv_mode==0):
		# ----------------- 0) value -----------------
		tx_data = "samuel"
	else:
		# ----------------- 1) key:value --------------
		key_str = 'id'
		tx_data = key_str    

	query_json['data']='"' + tx_data +'"'
	test_query(query_json)


	#==================== test tx commit ====================
	tx_json = {}
	tx_size = 128*1024
	tx_value = TypesUtil.string_to_hex(os.urandom(tx_size))

	if(kv_mode==0):
		# ----------------- 1) value --------------
		# tx_data = "samuel" 
		tx_data = tx_value
	else:
		# ----------------- 2) key:value --------------
		json_value={}
		json_value['name']="samuel_xu999"
		json_value['age']=36
		key_str = 'id'
		value_str = TypesUtil.json_to_tx(json_value)  
		# print(value_str) 

		# In tx_data, " must replace with ', for json: 'id={\'address\':\'hamilton\'}' 
		tx_data = key_str + "=" + value_str 

	# --------- build parameter string: tx=? --------
	tx_json['tx']='"' + tx_data +'"' 
	# print(tx_json)

	start_time=time.time()
	# ---------------- deliver tx --------------
	test_tx_commit(tx_json)
	exec_time=time.time()-start_time
	print(format(exec_time*1000, '.3f'))
	FileUtil.save_testlog('test_results', 'exec_time.log', format(exec_time*1000, '.3f'))

	pass
