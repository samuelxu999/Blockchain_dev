'''
========================
utilities.py
========================
Created on Oct.23, 2017
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide utility function to support project.
@Reference: 
'''

from datetime import datetime, timedelta
import json

'''
FileUtil class for handling file data
'''
class FileUtil(object):

	'''
	Function:read line contents from file
	@arguments: 
	(in)  filepath:   	input file path
	(out) ls_lines:   	return line list object
	'''
	@staticmethod
	def ReadLines(filepath):
		#define file handle to open select file
		fname = open(filepath, 'r')    
		#read text by line and saved as array list ls_lines
		ls_lines=fname.readlines()
		#close file
		fname.close()
		return ls_lines
	
	'''
	Function: write line string to file
	@arguments: 
	(in)  filepath:   	input file path
	(in)  linedata:   	line data for writing
	'''
	@staticmethod
	def AddLine(filepath, linedata):
		#define file handle to open select file for appending data
		fname = open(filepath, 'a') 
		
		#write line data to file
		fname.write("%s\n" %(linedata))
		
		#close file
		fname.close()
	
	'''
	Function: write list data to file by each line
	@arguments: 
	(in)  filepath:   	input file path
	(in)  ls_data:   	list data for writing
	'''
	@staticmethod
	def AddDataByLine(filepath, ls_data):
		#define file handle to open select file for write data
		fname = open(filepath, 'w') 
		
		#for each lines in data and write to file
		for linedata in ls_data:
			#write line data to file
			fname.write("%s\n" %(linedata))
		
		#close file
		fname.close()
	
	'''
	Function: remove line containing target string from file
	@arguments: 
	(in)  filepath:   	input file path
	(in)  str_target:   target string for delete
	'''
	@staticmethod
	def DeleteLine(filepath, str_target):
		#First, read all data from file
		fname = open(filepath, 'r')   
		ls_lines=fname.readlines()	
		fname.close()	

		#reopen file with 'w' option
		fname = open(filepath, 'w')
		
		#for each line to rewrite all data except ls_data
		for line in ls_lines:
			if((str_target in line) or line=='\n'):
				continue
			#write line data to file
			fname.write("%s" %(line))
		#close file
		fname.close()

	'''
	Function: update line containing target string in file
	@arguments: 
	(in)  filepath:   	input file path
	(in)  str_target:   target string for delete
	'''		
	@staticmethod
	def UpdateLine(filepath, str_target, str_line):
		#First, read all data from file
		fname = open(filepath, 'r')   
		ls_lines=fname.readlines()	
		fname.close()	

		#reopen file with 'w' option
		fname = open(filepath, 'w')
		
		#for each line to rewrite all data
		for line in ls_lines:
			if(str_target in line):
				#write updated data to file
				fname.write("%s" %(str_line))
			else:
				#write unchanged line to file
				fname.write("%s" %(line))
		#close file
		fname.close()
		
'''
DatetimeUtil class for format handle between datatime and string
'''
class DatetimeUtil(object):
	#switch int timestamp to datatime object
	@staticmethod
	def timestamp_datetime(_timestamp):
		obj_datetime=datetime.fromtimestamp(_timestamp/1e3)
		return obj_datetime

	#switch datatime object to int timestamp
	@staticmethod
	def datetime_timestamp(_datetime):
		int_datetime=int(_datetime.timestamp() * 1e3)
		return int_datetime

	#switch datatime object to format string
	@staticmethod
	def datetime_string(_datetime, _format="%Y-%m-%d %H:%M:%S"):
		str_datetime=_datetime.strftime(_format)
		return str_datetime
		
	#switch format string to datatime object
	@staticmethod
	def string_datetime(_strtime, _format="%Y-%m-%d %H:%M:%S"):
		_datetime=datetime.strptime(_strtime, _format)
		return _datetime
		
	#get datatime duration from format input
	@staticmethod
	def datetime_duration(_weeks=0,_days=0,_hours=0,_minutes=0):
		_duration=timedelta(weeks=_weeks,days=_days,hours=_hours,minutes=_minutes)
		return _duration
		
	#check whether input datatime has expired
	@staticmethod
	def IsExpired(str_datatime):
		time1=DatetimeUtil.string_datetime(str_datatime)
		time2=datetime.now()
		diff = (time1-time2).total_seconds()
		if(diff>0):
			return False
		else:
			return True
			
'''
TypesUtil class for data type format transfer
'''
class TypesUtil(object):
	#string to hex
	@staticmethod
	def string_to_hex(str_data):
		hex_data=str_data.hex()
		return hex_data
		
	#hex to string
	@staticmethod
	def hex_to_string(hex_data):
		str_data=bytes.fromhex(hex_data)
		return str_data
		
	#string to bytes
	@staticmethod
	def string_to_bytes(str_data):
		bytes_data=str_data.encode(encoding='UTF-8')
		return bytes_data
		
	#bytes to string
	@staticmethod
	def bytes_to_string(byte_data):
		str_data=byte_data.decode(encoding='UTF-8')
		return str_data
		
	#string to json
	@staticmethod
	def string_to_json(json_str):
		json_data = json.loads(json_str)
		return json_data
		
	#json to string
	@staticmethod
	def json_to_string(json_data):
		json_str = json.dumps(json_data)
		return json_str

	#json list to string
	@staticmethod
	def jsonlist_to_string(json_list):
		list_str="|".join(TypesUtil.json_to_string(e) for e in json_list)
		return list_str

	#string to json list
	@staticmethod
	def string_to_jsonlist(str_data):
		list_data=str_data.split('|')
		json_list=[]
		for data in list_data: 
			json_list.append(TypesUtil.string_to_json(data))
		return json_list
