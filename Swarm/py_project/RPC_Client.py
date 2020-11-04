#!/usr/bin/env python3

'''
========================
PRC_Client module
========================
Created on Nov.4, 2020
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of RPC-JSON API that access to local Swarm node.
@Install  pycurl packages: pip install pycurl
@Reference: https://swarm-guide.readthedocs.io/en/latest/dapp_developer/index.html
'''

import requests
import json
import time
import os
import pycurl
from io import BytesIO 
from utilities import TypesUtil,FileUtil

class PRC_Client(object):

	'''
	This can save a string data on swarm
	Execute curl -X POST -H "Content-Type: text/plain" --data "some-data" http://localhost:8500/bzz:/
	Return: Swarm hash of the address string of your content inside Swarm.
	'''
	@staticmethod
	def upload_string(json_data): 

		# save data in byte_buffer with utf-8 format 
		data = json_data['data']

		# set body buffer to save response information
		body_buffer = BytesIO(data.encode('utf-8')) 

		crl = pycurl.Curl()

		crl.setopt(crl.HTTPHEADER, ['Content-Type: text/plain'])

		# Set URL value
		crl.setopt(crl.URL, 'http://localhost:8500/bzz:/')

		crl.setopt(crl.POST, 1)

		crl.setopt(crl.POSTFIELDS, data)

		# Write response data into body_buffer
		crl.setopt(crl.WRITEDATA, body_buffer)

		# Perform a file transfer 
		crl.perform() 

		# End curl session
		crl.close()

		# Get the content stored in the BytesIO object (in byte characters) 
		get_body = body_buffer.getvalue()

		# Decode the bytes stored in get_body and return the result 
		swarm_hash = get_body.decode('utf8')

		return swarm_hash

	'''
	To download a string content from Swarm, you just need the string’s Swarm hash. 
	curl http://localhost:8500/bzz:/@hash/
	'''
	@staticmethod
	def download_string(swarm_hash): 

		data_buffer = BytesIO() 
		crl = pycurl.Curl()

		# Set URL value
		crl.setopt(crl.URL, 'http://localhost:8500/bzz:/'+swarm_hash+'/')

		# Write bytes that are utf-8 encoded
		crl.setopt(crl.WRITEDATA, data_buffer)

		# Perform a file transfer 
		crl.perform() 

		# End curl session
		crl.close()

		# Get the content stored in the BytesIO object (in byte characters) 
		get_body = data_buffer.getvalue()

		# Decode the bytes stored in get_body and return the result 
		return get_body.decode('utf8')


if __name__ == "__main__":

	#==================== test upload string =========================
	tx_json = {}
	# tx_size = 128*1024
	# tx_data = TypesUtil.string_to_hex(os.urandom(tx_size))

	kv_mode = 1
	if(kv_mode==0):
		# ----------------- 1) value --------------
		tx_data = "This is samuel test message!"
	else:
		# ----------------- 2) key:value --------------
		json_value={}
		json_value['id']='1'
		json_value['name']="samuel_xu"
		json_value['age']=28
		tx_data = TypesUtil.json_to_string(json_value)  
	
	tx_json['data']=tx_data

	post_ret = PRC_Client.upload_string(tx_json)
	print(post_ret)

	#==================== test download string =========================
	query_json = {}

	# use string hash
	# swarm_hash = '4c9293963f4c1e9b7cd3e9e3a45d41ec8a961278be2701ce071317d4832d3bca'
	swarm_hash = post_ret

	query_ret = PRC_Client.download_string(swarm_hash)
	print(query_ret)

	pass
