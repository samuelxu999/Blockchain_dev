#!/usr/bin/env python3.5

'''
========================
WS_Client module
========================
Created on Nov.2, 2017
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of client API that access to Web service.
'''
import time
import requests
import datetime
import json

from CapAC_Token import CapACToken

import sys
from utilities import DatetimeUtil, TypesUtil, FileUtil

now = datetime.datetime.now()
datestr=now.strftime("%Y-%m-%d")
timestr=now.strftime("%H:%M:%S")
    
class WSClient(object):
    
    '''
    Get all dataset
    '''
    @staticmethod
    def Get_Datasets(api_url, data_args={}):          
        headers = {'Content-Type' : 'application/json'}
        response = requests.get(api_url, data=json.dumps(data_args), headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response
    
    '''
    Get record by id
    '''
    @staticmethod
    def Get_DataByID(api_url, params, data_args={} ):          
        headers = {'Content-Type' : 'application/json'}
        response = requests.get(api_url,params=params, data=json.dumps(data_args), headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response
    
    '''
    Post data to add record
    '''
    @staticmethod
    def Create_Data(api_url, data):          
        headers = {'Content-Type' : 'application/json'}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response
    
    '''
    Put updated data
    '''
    @staticmethod
    def Update_Data(api_url, data):          
        headers = {'Content-Type' : 'application/json'}
        response = requests.put(api_url, data=json.dumps(data), headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response
    
    '''
    Put id to delete data
    '''
    @staticmethod
    def Delete_Data(api_url, data):          
        headers = {'Content-Type' : 'application/json'}
        response = requests.delete(api_url, data=json.dumps(data), headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response

def test_search(data_args={}):
	params={}
	if('project_id' in data_args):
		params['project_id']=data_args['project_id']
	else:
		params['project_id']=0

	print(WSClient.Get_Datasets('http://128.226.78.89/test/api/v1.0/dt', data_args))
	#print(WSClient.Get_DataByID('http://128.226.78.89/test/api/v1.0/dt/project', params, data_args))
    
def test_add(data_args={}):
	project = {
		'title': 'post_new',
		'description': 'post_description',
		'date': datestr,
		'time': timestr
	}
	project_data = {'project_data':project}
	
	if(bool(data_args)):
		project_data['token_data']=data_args['token_data']
	json_response=WSClient.Create_Data('http://128.226.78.217/test/api/v1.0/dt/create',project_data)
	#print(json_response['project_data'])
	print(json_response)
    
def test_update(data_args={}):
	project = {
		'id': 2,
		'title': 'update_test',
		'description': 'update_description',
		'date': datestr,
		'time': timestr
	}		
	project_data = {'project_data':project}

	if(bool(data_args)):
		project_data['token_data']=data_args['token_data']
		
	json_response=WSClient.Update_Data('http://128.226.78.217/test/api/v1.0/dt/update',project_data)
	print(json_response)
    
def test_delete(data_args={}):
	project_data = {'id': 3}

	if(bool(data_args)):
		project_data['token_data']=data_args['token_data']

	json_response=WSClient.Delete_Data('http://128.226.78.217/test/api/v1.0/dt/delete',project_data)
	print(json_response)

	
def test_CapAC():
	
	#params = {'project_id':'2'}
	data_args = {'project_id':'2'}
	
	start_time=time.time()
	
	#print token_data	
	#test_add(data_args)
	#test_update(data_args)
	#test_delete(data_args)	
	test_search(data_args)
	
	end_time=time.time()
	exec_time=end_time-start_time
	
	time_exec=format(exec_time*1000, '.3f')
	print("Execution time is:%2.6f" %(exec_time))

	FileUtil.AddLine('exec_time_client.log', time_exec)
	'''print WSClient.Get_Datasets('http://128.226.78.217/test/api/v1.0/dt', data_args)
	print WSClient.Get_DataByID('http://128.226.78.217/test/api/v1.0/dt/project',params, data_args)'''

if __name__ == "__main__":
	'''test_search()
	test_add()
	test_update()
	test_delete()
	test_token()'''
	test_CapAC()
	pass
