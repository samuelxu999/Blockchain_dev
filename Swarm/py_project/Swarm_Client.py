#!/usr/bin/env python

'''
========================
Swarm_Client module
========================
Created on Nov.23, 2020
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of client API that access to Swarm server node.
                  Mainly used to test and demo.
'''
import argparse
import sys
import os
import requests
import json
import time
import logging

from utilities import TypesUtil, FileUtil


logger = logging.getLogger(__name__)

# ====================================== client side REST API ==================================

def test_download_data(target_address, swarm_hash):
	headers = {'Content-Type' : 'application/json'}
	api_url = 'http://'+target_address+'/swarm/data/download'
	data_args = {}
	data_args['hash']=swarm_hash

	response = requests.get(api_url, data=json.dumps(data_args), headers=headers)

	json_results = {}
	json_results['status']=response.status_code
	if(json_results['status']==200):
		json_results['data']=response.json()['data']
	else:
		json_results['data']=''
	# logger.info(json_results)

	return json_results


def test_upload_data(target_address, tx_json):
	headers = {'Content-Type' : 'application/json'}
	api_url = 'http://'+target_address+'/swarm/data/upload'
	data_args = {}
	data_args['data']=tx_json

	response = requests.post(api_url, data=json.dumps(data_args), headers=headers)

	json_results = {}
	json_results['status']=response.status_code
	if(json_results['status']==200):
		json_results['data']=response.json()['data']
	else:
		json_results['data']=''
	# logger.info(json_results)

	return json_results

def test_download_file(target_address, swarm_hash, file_name, download_file='download_data'):
	headers = {'Content-Type' : 'application/json'}
	api_url = 'http://'+target_address+'/swarm/file/download'
	data_args = {}
	data_args['hash']=swarm_hash
	data_args['file_name']=file_name
	data_args['download_file']=download_file

	response = requests.get(api_url, data=json.dumps(data_args), headers=headers)

	json_results ={}
	json_results['status'] = response.status_code
	if(json_results['status']==200):
		file_handle = open(download_file, 'wb')
		file_handle.write(response.content)
		file_handle.close()

		json_results['data']="Download: {} from address: {} to local as: {}".format(file_name, swarm_hash, download_file)
	else:
		json_results['data']=response.json()
	# logger.info(json_results)

	return json_results

def test_upload_file(target_address, tx_json):
	api_url = 'http://'+target_address+'/swarm/file/upload'

	files = {'uploaded_file': open(tx_json['upload_file'],'rb')}

	response = requests.post(api_url, files=files)

	json_results = {}
	json_results['status']=response.status_code
	if(json_results['status']==200):
		json_results['data']=response.json()['data']
	else:
		json_results['data']=''
	# logger.info(json_results)

	return json_results

def define_and_get_arguments(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(
		description="Run swarm websocket client."
	)
	parser.add_argument("--test_fun", type=int, default=0, help="test function option.")
	parser.add_argument("--op_status", type=int, default=0, help="operation status in current function.")
	parser.add_argument("--kv_mode", type=int, default=0, help="tx data format: string or json.")
	parser.add_argument("--test_round", type=int, default=1, help="test evaluation round")
	parser.add_argument("--wait_interval", type=int, default=1, help="break time between step.")
	parser.add_argument("--target_address", type=str, default="0.0.0.0:8501", 
						help="Test target address - ip:port.")
	args = parser.parse_args(args=args)
	return args


if __name__ == "__main__":
	FORMAT = "%(asctime)s %(levelname)s | %(message)s"
	LOG_LEVEL = logging.INFO
	logging.basicConfig(format=FORMAT, level=LOG_LEVEL)

	# get arguments
	args = define_and_get_arguments()

	# set parameters
	target_address = args.target_address
	test_fun = args.test_fun
	op_status = args.op_status
	kv_mode = args.kv_mode
	wait_interval = args.wait_interval
	test_run = args.test_round
	tx_json = {}

	# |------------------------ test case type ---------------------------------|
	# | 0: data transfer  | 1: file transfer |
	# |-------------------------------------------------------------------------|

	if(test_fun == 0):

		#==================== test upload data =========================
		if(kv_mode==0):
			# ----------------- 1) value --------------
			# tx_size = 128
			# tx_data = TypesUtil.string_to_hex(os.urandom(tx_size))
			tx_data = "This is samuel test message!"
		else:
			# ----------------- 2) key:value --------------
			json_value={}
			json_value['id']='1'
			json_value['name']="samuel_xu"
			json_value['age']=28
			tx_data = TypesUtil.json_to_string(json_value)  
		
		tx_json['data']=tx_data
		post_ret = test_upload_data(target_address, tx_json)
		print(post_ret)

		#==================== test download data =========================
		# swarm_hash = '4c9293963f4c1e9b7cd3e9e3a45d41ec8a961278be2701ce071317d4832d3bca'
		swarm_hash = post_ret['data']
		query_ret = test_download_data(target_address,swarm_hash)
		print(query_ret)
	elif(test_fun == 1):
		#==================== test upload file =========================
		if(op_status==0):
			file_name = "test_data.txt"
		else:
			file_name = "mnist_cnn.pt"

		tx_json['upload_file']=file_name
		post_ret =test_upload_file(target_address, tx_json)
		print(post_ret)

		#==================== test download file =========================
		# swarm_hash = '683b0a7918fbad1763fe0baccf7df1ef0fffc342c1b12abdecf57c009135eeb2'
		swarm_hash = post_ret['data']

		query_ret = test_download_file(target_address, swarm_hash, file_name)
		print(query_ret)
	else:
		pass
