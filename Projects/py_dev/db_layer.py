#!/usr/bin/env python3.5

'''
========================
db_layer.py
========================
Created on Mar.24, 2018
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide database layer API.
@Reference: https://www.sqlite.org/
'''

import sqlite3
from utilities import DatetimeUtil, TypesUtil, FileUtil

# returning an object that can also access columns by name
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

'''
UsersManager class for manage database by using SQLite lib
'''
class UsersManager(object):

	#Create table in db file
	@staticmethod	
	def create_table(db_path):
		conn = sqlite3.connect(db_path)
		
		#check whether table already exists
		cursor = conn.execute("SELECT name from sqlite_master where Type='table' and name='Userdata';")
		row_count=0
		for row in cursor:
			row_count+=1

		if(row_count==0):
			#create table
			conn.execute("CREATE TABLE Userdata \
					 (Name           		TEXT PRIMARY KEY, \
					 Address        		TEXT    	NULL, \
					 Role           		TEXT    	NULL, \
					 ExpireTime         	TEXT    	NOT NULL);")
		else:
			print("Table:Userdata already exists.")

	#Remove table
	def remove_table(db_path):
		conn = sqlite3.connect(db_path)
		#remove selected table
		cursor = conn.execute("DROP TABLE Userdata;")


	#Select all record from table
	@staticmethod		
	def select_Allentry(path_db):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT Name, Address, Role, ExpireTime from Userdata;")

		ls_result=[]
		for row in cursor:	
			ls_result.append(row)

		conn.close()
		
		return ls_result

	#Select record from table based on Name
	@staticmethod		
	def select_ByName(path_db, user_name):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT Name, Address, Role, ExpireTime from Userdata where Name='%s';" %(user_name))
		
		ls_result=[]		
		for row in cursor:
			ls_result.append(row)
			
		conn.close()
		
		return ls_result

	#Insert user entry into Userdata
	@staticmethod	
	def insert_entry(path_db, arg_list):	
		conn = sqlite3.connect(path_db)

		#check if user name already exist
		user_entry=UsersManager.select_ByName(path_db, arg_list[0])
		if(len(user_entry)>0):
			print("%s already exists!" %(arg_list[0]))
		else:			  
			conn.execute("INSERT INTO Userdata (Name, Address, Role, ExpireTime) VALUES ('%s', '%s','%s','%s');" \
				%(arg_list[0], arg_list[1], arg_list[2], arg_list[3]));

			conn.commit()
		conn.close()

	#Update record of Userdata based on name
	@staticmethod	
	def update_entry(path_db, arg_list):
		conn = sqlite3.connect(path_db)
		
		conn.execute("UPDATE Userdata set Address='%s', Role='%s', ExpireTime='%s' where Name='%s';" \
					%(arg_list[1], arg_list[2], arg_list[3], arg_list[0]))
		
		conn.commit()
		conn.close()

	#Delete user from Userdata based on Name
	@staticmethod		
	def delete_ByName(path_db, user_name):
		conn = sqlite3.connect(path_db)

		conn.execute("DELETE from Userdata where Name = '%s';" %(user_name))
		conn.commit()
		
		conn.close()

'''
RolesManager class for manage database by using SQLite lib
'''
class RolesManager(object):

	#Create table in db file
	@staticmethod	
	def create_table(db_path):
		conn = sqlite3.connect(db_path)
		
		#check whether table already exists
		cursor = conn.execute("SELECT name from sqlite_master where Type='table' and name='Roledata';")
		row_count=0
		for row in cursor:
			row_count+=1

		if(row_count==0):
			#create table
			conn.execute("CREATE TABLE Roledata \
					 (Name           		TEXT    	PRIMARY KEY, \
					 AccessRight       		TEXT    	NOT NULL);")
		else:
			print("Table:Roledata already exists.")

	#Remove table
	def remove_table(db_path):
		conn = sqlite3.connect(db_path)
		#remove selected table
		cursor = conn.execute("DROP TABLE Roledata;")

	#Select all record from table
	@staticmethod		
	def select_Allentry(path_db):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT Name, AccessRight from Roledata;")
		
		ls_result=[]
		for row in cursor:			
		   ls_result.append(row)

		conn.close()
		
		return ls_result

	#Select record from table based on Name
	@staticmethod		
	def select_ByName(path_db, role_name):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT Name, AccessRight from Roledata where Name='%s';" %(role_name))
		
		ls_result=[]		
		for row in cursor:
			ls_result.append(row)
			
		conn.close()
		
		return ls_result

	#Insert user entry into Userdata
	@staticmethod	
	def insert_entry(path_db, arg_list):	
		conn = sqlite3.connect(path_db)

		#check if user name already exist
		user_entry=RolesManager.select_ByName(path_db, arg_list[0])
		if(len(user_entry)>0):
			print("%s already exists!" %(arg_list[0]))
		else:			  
			conn.execute("INSERT INTO Roledata (Name, AccessRight) VALUES ('%s', '%s');" \
						%(arg_list[0], arg_list[1]));

			conn.commit()
		conn.close()

	#Update record of Userdata based on name
	@staticmethod	
	def update_entry(path_db, arg_list):
		conn = sqlite3.connect(path_db)
		
		conn.execute("UPDATE Roledata set AccessRight='%s' where Name='%s';" \
					%(arg_list[1], arg_list[0]))
		
		conn.commit()
		conn.close()

	#Delete user from Userdata based on Name
	@staticmethod		
	def delete_ByName(path_db, role_name):
		conn = sqlite3.connect(path_db)

		conn.execute("DELETE from Roledata where Name = '%s';" %(role_name))
		conn.commit()
		
		conn.close()

'''
AccessManager class for manage database by using SQLite lib
'''
class AccessManager(object):

	#Select all record from table by join user and role table
	@staticmethod		
	def select_Allentry(path_db):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT Userdata.Name, Userdata.Address, Userdata.ExpireTime, Userdata.Role, Roledata.AccessRight \
								from Userdata \
								Inner join Roledata \
								on Userdata.Role=Roledata.Name \
								order by Userdata.Name;")

		ls_result=[]
		for row in cursor:			
		   ls_result.append(row)

		conn.close()
		
		return ls_result

	#Select record from table based on Name
	@staticmethod		
	def select_ByName(path_db, user_name):		
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT Userdata.Name, Userdata.Address, Userdata.ExpireTime, Userdata.Role, Roledata.AccessRight \
								from Userdata \
								Inner join Roledata \
								on Userdata.Role=Roledata.Name \
								where Userdata.Name='%s' \
								order by Userdata.Name;" %(user_name))

		ls_result=[]
		for row in cursor:			
		   ls_result.append(row)

		conn.close()
		
		return ls_result

'''
ABACRuleManager class for manage ABAC rules database by using SQLite lib
'''
class ABACRuleManager(object):

	#Create table in db file
	@staticmethod	
	def create_table(db_path):
		conn = sqlite3.connect(db_path)
		
		#check whether table already exists
		cursor = conn.execute("SELECT name from sqlite_master where Type='table' and name='ABACRules';")
		row_count=0
		for row in cursor:
			row_count+=1

		if(row_count==0):
			#create table
			conn.execute("CREATE TABLE ABACRules \
					 (Name           	TEXT 		PRIMARY KEY, \
					 AttrUser           TEXT 		NOT NULL, \
					 AttrAction        	TEXT    	NOT NULL, \
					 AttrResource      	TEXT    	NOT NULL, \
					 AttrEnvironment    TEXT    	NOT NULL);")
		else:
			print("Table:ABACRules already exists.")

	#Remove table
	def remove_table(db_path):
		conn = sqlite3.connect(db_path)
		#remove selected table
		cursor = conn.execute("DROP TABLE ABACRules;")

	#Select all record from table
	@staticmethod		
	def select_Allentry(path_db):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT * from ABACRules;")

		ls_result=[]
		for row in cursor:	
			ls_result.append(row)

		conn.close()
		
		return ls_result

	#Select record from table based on Name
	@staticmethod		
	def select_ByName(path_db, rule_name):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory
		cursor = conn.execute("SELECT * from ABACRules where Name='%s';" %(rule_name))
		
		ls_result=[]		
		for row in cursor:
			ls_result.append(row)
			
		conn.close()
		
		return ls_result

	#Select record from table based on field Name and value 
	@staticmethod		
	def select_ByFieldname(path_db, field_data):
		conn = sqlite3.connect(path_db)	
		conn.row_factory = dict_factory

		SQL_cmd="SELECT * from ABACRules where "

		i=0
		for key, value in field_data.items(): 
			#print(key, value)
			if(i>0):
				SQL_cmd+=(" and ")
			SQL_cmd+=("%s='%s'" %(key, value))
			i+=1
		#print(SQL_cmd)
		cursor = conn.execute(SQL_cmd)
		ls_result=[]		
		for row in cursor:
			ls_result.append(row)
			
		conn.close()
		
		return ls_result

	#Insert rule entry into ABACRules table
	@staticmethod	
	def insert_entry(path_db, arg_list):	
		conn = sqlite3.connect(path_db)

		#check if rule name already exist
		rule_entry=ABACRuleManager.select_ByName(path_db, arg_list['Name'])
		if(len(rule_entry)>0):
			print("%s already exists!" %(arg_list['Name']))
		else:
			conn.execute("INSERT INTO ABACRules (Name, AttrUser, AttrAction, AttrResource, AttrEnvironment) \
						VALUES ('%s', '%s','%s','%s', '%s');" \
						%(	arg_list['Name'], \
							arg_list['AttrUser'], \
							arg_list['AttrAction'], \
							arg_list['AttrResource'], \
							arg_list['AttrEnvironment']))

			conn.commit()
		conn.close()

	#Update record of ruledata based on name
	@staticmethod	
	def update_entry(path_db, arg_list):
		conn = sqlite3.connect(path_db)
		
		conn.execute("UPDATE ABACRules \
						set AttrUser='%s', AttrAction='%s', AttrResource='%s', AttrEnvironment='%s' \
						where Name='%s';" \
						%(	arg_list['AttrUser'], \
							arg_list['AttrAction'], \
							arg_list['AttrResource'], \
							arg_list['AttrEnvironment'], \
							arg_list['Name']))
		
		conn.commit()
		conn.close()

	#Delete rule from ABACRules based on Name
	@staticmethod		
	def delete_ByName(path_db, rule_name):
		conn = sqlite3.connect(path_db)

		conn.execute("DELETE from ABACRules where Name = '%s';" %(rule_name))
		conn.commit()
		
		conn.close()

def test_user():
	#test Api
	path_db='RBAC.db'
	# new Userdata table 
	UsersManager.create_table(path_db)
	#UsersManager.remove_table(path_db)

	# test insert user data
	user_arg1=['lenovo_miner1_0', '0x3d40fad73c91aed74ffbc1f09f4cde7cce533671', 'admin', '2018-5-28 11:29:42']
	user_arg2=['RPi1_node_0', '0xaa09c6d65908e54bf695748812c51d8f2ceea0f5', 'no', '2018-11-8 18:39:42']
	UsersManager.insert_entry(path_db,user_arg1)
	UsersManager.insert_entry(path_db,user_arg2)

	#search test
	users_list=UsersManager.select_Allentry(path_db)
	print(users_list)
	user_entry=UsersManager.select_ByName(path_db,'RPi1_node_0')
	print(user_entry)

	#update test
	update_arg1=['RPi1_node_0', '0xaa09c6d65908e54bf695748812c51d8f2ceea0f5', 'viewer', '2018-11-8 18:39:42']
	UsersManager.update_entry(path_db,update_arg1)
	print(UsersManager.select_ByName(path_db,update_arg1[0]))

	#delete test
	#UsersManager.delete_ByName(path_db,user_arg1[0])
	print(UsersManager.select_ByName(path_db,user_arg1[0]))

def generateAdmin():
	#get access right
	role_arg=[]
	role_arg.append('admin')

	#construct access json data 
	ac_list=[]
	#access right 1
	ac_json={}
	ac_json['resource']='/test/api/v1.0/dt'
	ac_json['action']='GET'
	ac_json['conditions']={}
	#construct condition json data
	ac_json['conditions']['value']={}
	ac_json['conditions']['value']['start']='16:12:32'
	ac_json['conditions']['value']['end']='23:32:32'
	ac_json['conditions']['type']='Timespan' 
	ac_list.append(ac_json)

	#access right 2
	ac_json={}
	ac_json['resource']='/test/api/v1.0/dt/project'
	ac_json['action']='GET'
	ac_json['conditions']={}
	#construct condition json data
	ac_json['conditions']['value']={}
	ac_json['conditions']['value']['start']='8:12:32'
	ac_json['conditions']['value']['end']='16:32:32'
	ac_json['conditions']['type']='Timespan' 
	ac_list.append(ac_json)

	#append json list to role_arg
	role_arg.append(TypesUtil.jsonlist_to_string(ac_list))
	return role_arg

def generateViewer():
	#get access right
	role_arg=[]
	role_arg.append('viewer')

	#construct access json data 
	ac_list=[]

	#access right 1
	ac_json={}
	ac_json['resource']='/test/api/v1.0/dt/project'
	ac_json['action']='GET'
	ac_json['conditions']={}
	#construct condition json data
	ac_json['conditions']['value']={}
	ac_json['conditions']['value']['start']='8:12:32'
	ac_json['conditions']['value']['end']='12:32:32'
	ac_json['conditions']['type']='Timespan' #TypesUtil.json_to_string(ac_json)
	ac_list.append(ac_json)

	#append json list to role_arg
	role_arg.append(TypesUtil.jsonlist_to_string(ac_list))
	return role_arg


def test_role():
	#test Api
	path_db='RBAC.db'
	# new Userdata table 
	RolesManager.create_table(path_db)
	#RolesManager.remove_table(path_db)

	# test insert user data
	role_arg1=['admin', '{"resource": "/test/api/v1.0/dt", "action": "GET", "conditions": {"value": {"start": "8:12:32", "end": "14:32:32"}, "type": "Timespan"}}, \
				{"resource": "/test/api/v1.0/dt/project", "action": "GET", "conditions": {"value": {"start": "13:12:32", "end": "19:32:32"}, "type": "Timespan"}}']
	role_arg2=['viewer', '{"resource": "/test/api/v1.0/dt/project", "action": "GET", "conditions": {"value": {"start": "13:12:32", "end": "19:32:32"}, "type": "Timespan"}}']
	RolesManager.insert_entry(path_db,role_arg1)
	RolesManager.insert_entry(path_db,role_arg2)

	#search test
	roles_list=RolesManager.select_Allentry(path_db)
	print(roles_list)
	role_entry=RolesManager.select_ByName(path_db,'admin')
	print(role_entry)

	#update test
	update_arg1=['viewer', '{"resource": "/test/api/v1.0/dt/create", "action": "POST", "conditions": {"value": {"start": "17:12:32", "end": "19:32:32"}, "type": "Timespan"}}']
	RolesManager.update_entry(path_db,update_arg1)
	print(RolesManager.select_ByName(path_db,update_arg1[0]))

	#delete test
	#RolesManager.delete_ByName(path_db,role_arg1[0])
	print(RolesManager.select_ByName(path_db,role_arg1[0]))

def test_access():
	#test Api
	path_db='RBAC.db'

	user_list=UsersManager.select_Allentry(path_db)
	print(user_list)

	#get access right
	'''role_admin=generateAdmin()
	role_viewer=generateViewer()
	print(role_admin)
	print(role_viewer)

	#update role data to database
	RolesManager.update_entry(path_db,role_admin)
	RolesManager.update_entry(path_db,role_viewer)'''

	#load data from database
	#user_access=AccessManager.select_Allentry(path_db)
	user_access=AccessManager.select_ByName(path_db, user_list[1]['Name'])
	print(user_access)

	#read access right data
	json_data=TypesUtil.string_to_jsonlist(user_access[0]['AccessRight'])
	print(json_data)
	print(json_data[0]['conditions']['value']['start'])

def test_ABACRules():
	#test Api
	path_db='ABAC.db'
	# new Userdata table 
	ABACRuleManager.create_table(path_db)
	#ABACRuleManager.remove_table(path_db)

	#test insert user data
	rule_arg = {}
	rule_arg['Name'] = "rule2"
	rule_arg['AttrUser'] = "admin"
	rule_arg['AttrAction'] = "GET"
	rule_arg['AttrResource'] = "/test/api/v1.0/dt"
	#define environmental attribute
	env_time={}
	env_time['type']='Timespan'
	env_time['value']={}
	env_time['value']['start']='14:12:32'
	env_time['value']['end']='23:12:32'
	rule_arg['AttrEnvironment'] = TypesUtil.json_to_string(env_time)
	ABACRuleManager.insert_entry(path_db,rule_arg)

	#search test
	rules_list=ABACRuleManager.select_Allentry(path_db)
	print(rules_list)
	print(TypesUtil.string_to_json(rules_list[0]['AttrEnvironment'])['type'])
	rules_entry = ABACRuleManager.select_ByName(path_db, 'rule1')
	print(rules_entry)
	
	#build up fields condition
	field_data = {}
	#field_data['Name'] = "rule1"
	field_data['AttrUser'] = "admin"
	field_data['AttrAction'] = "GET"
	field_data['AttrResource'] = "/test/api/v1.0/dt/project"
	#define environmental attribute
	env_time={}
	env_time['type']='Timespan'
	env_time['value']={}
	env_time['value']['start']='8:12:32'
	env_time['value']['end']='14:12:32'
	#field_data['AttrEnvironment'] = TypesUtil.json_to_string(env_time)	
	#rules_entry = ABACRuleManager.select_ByFieldname(path_db, field_data)
	#print(rules_entry)

	#update test
	update_arg=rule_arg
	update_arg['AttrUser']="admin"
	update_arg['AttrResource']="/test/api/v1.0/dt/project"
	env_update=TypesUtil.string_to_json(update_arg['AttrEnvironment'])
	env_update['value']['start']="13:12:32"
	env_update['value']['end']="22:12:32"
	#update_arg['AttrEnvironment']= TypesUtil.json_to_string(env_update)
	#ABACRuleManager.update_entry(path_db,update_arg)
	#print(ABACRuleManager.select_ByName(path_db,update_arg['Name']))

	#delete test
	#ABACRuleManager.delete_ByName(path_db,rule_arg['Name'])
	#print(ABACRuleManager.select_ByName(path_db,rule_arg['Name']))


if __name__ == '__main__': 
	#test_user()
	#test_role()
	#test_access()
	test_ABACRules()

	pass


