#!/usr/bin/env python

'''
========================
Swarm_Server module
========================
Created on Nov.23, 2020
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of swarm node API that handle and response client's request.
                  This can be used as a swarm service provider.
'''
import sys
import os
import json
import logging
from flask import Flask, jsonify, send_from_directory, send_file
from flask import abort,make_response,request
from argparse import ArgumentParser

from utilities import FileUtil, TypesUtil
from RPC_Client import RPC_Curl

logger = logging.getLogger(__name__)

# ================================= Instantiate the server =====================================
app = Flask(__name__)
#CORS(app)

#===================================== swarm node RPC handler ===================================
@app.route('/swarm/data/download', methods=['GET'])
def download_data():
	# parse data from request.data
	req_data=TypesUtil.bytes_to_string(request.data)

	tx_json=json.loads(req_data)

	if(tx_json=={}):
		abort(401, {'error': 'No parameter data'})

	# -------------- call curl API to query data ------------------
	swarm_hash = tx_json['hash']
	query_ret = rpc_curl.download_string(swarm_hash)

	response = {}
	# build response given get result
	if(query_ret['status']==200):
		response['data'] = query_ret['results']
	else:
		response['data'] = ''

	return jsonify(response), 200

@app.route('/swarm/data/upload', methods=['POST'])
def upload_data():
	# parse data from request.data
	req_data=TypesUtil.bytes_to_string(request.data)

	tx_json=json.loads(req_data)['data']
	
	if(tx_json=={}):
		abort(401, {'error': 'No parameter data'})

	# -------------- call curl API to send data ------------------
	post_ret = rpc_curl.upload_string(tx_json)
	
	response = {}
	# build response given post result
	if(post_ret['status']==200):
		response['data'] = post_ret['results']
	else:
		response['data'] = ''

	return jsonify(response), 200

@app.route('/swarm/file/download', methods=['GET'])
def download_file():
	# parse data from request.data
	req_data=TypesUtil.bytes_to_string(request.data)

	tx_json=json.loads(req_data)

	if(tx_json=={}):
		abort(401, {'error': 'No parameter data'})

	# -------------- call curl API to query data ------------------
	swarm_hash = tx_json['hash']
	file_name = tx_json['file_name']
	download_file = tx_json['download_file']
	query_ret = rpc_curl.download_file(swarm_hash, file_name, download_file)

	response = {}
	# build response given query result
	if(query_ret['status']==200):
		# response['data'] = query_ret['results']
		return query_ret['content'], 200
	else:
		response['error'] = 'Cannot download file: {}'.format(file_name)
		return jsonify(response), 402

@app.route('/swarm/file/upload', methods=['POST'])
def upload_file():
	
	# parse files from request.files
	uploaded_file = request.files['uploaded_file']

	if(uploaded_file.filename == ''):
		abort(401, {'error': 'No file data'})
	
	file_name = uploaded_file.filename
	# save uploaded to local
	uploaded_file.save(file_name)

	# # -------------- call curl API to upload file to swarm net ------------------
	post_ret = rpc_curl.upload_file(file_name)

	# remove local uploaded file
	os.remove(file_name)
	
	response = {}
	# build response given query result
	if(post_ret['status']==200):
		response['data'] = post_ret['results']
	else:
		response['data'] = ''

	return jsonify(response), 200

def define_and_get_arguments(args=sys.argv[1:]):
	parser = ArgumentParser(description="Run swarm_server websocket server.")
	parser.add_argument('-p', '--port', default=8580, type=int, 
						help="port to listen on.")
	parser.add_argument('-bp', '--bzz_port', default=8500, type=int, 
						help="bzz port to listen on.")
	parser.add_argument("--debug", action="store_true", 
						help="if set, debug model will be used.")
	parser.add_argument("--threaded", action="store_true", 
						help="if set, support threading request.")
	args = parser.parse_args()

	return args

if __name__ == '__main__':
	# FORMAT = "%(asctime)s %(levelname)s %(filename)s(l:%(lineno)d) - %(message)s"
	FORMAT = "%(asctime)s %(levelname)s | %(message)s"
	LOG_LEVEL = logging.INFO
	logging.basicConfig(format=FORMAT, level=LOG_LEVEL)

	# get arguments
	args = define_and_get_arguments()

	rpc_curl = RPC_Curl(args.bzz_port)

	app.run(host='0.0.0.0', port=args.port, debug=args.debug, threaded=args.threaded)

