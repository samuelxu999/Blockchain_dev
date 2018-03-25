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
					 (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
					 Name           		TEXT    	NOT NULL, \
					 Address        		TEXT    	NULL, \
					 Role           		TEXT    	NULL, \
					 ExpireTime         	TEXT    	NOT NULL);")
		else:
			print("Userdata already exists.")

	#Remove table
	def remove_table(db_path, tb_name):
		conn = sqlite3.connect(db_path)
		#remove selected table
		cursor = conn.execute("DROP TABLE %s;" %(tb_name))


	#Select all record from table
	@staticmethod		
	def select_Allentry(path_db):
		conn = sqlite3.connect(path_db)	
	
		cursor = conn.execute("SELECT Name, Address, Role, ExpireTime from Userdata;")
		
		ls_result=[]
		for row in cursor:			
		   ls_result.append(row)

		conn.close()
		
		return ls_result

	#Select record from table based on Type
	@staticmethod		
	def select_ByName(path_db, user_name):
		conn = sqlite3.connect(path_db)	
	
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

def test_user():
	#test Api
	path_db='RBAC.db'
	# new Userdata table 
	UsersManager.create_table(path_db)
	#UsersManager.remove_table(path_db, 'Userdata')

	# test insert user data
	user_arg1=['lenovo_miner1_0', '0x3d40fad73c91aed74ffbc1f09f4cde7cce533671', 'Admin', '2018-5-28 11:29:42']
	user_arg2=['RPi1_node_0', '0xaa09c6d65908e54bf695748812c51d8f2ceea0f5', '', '2018-11-8 18:39:42']
	UsersManager.insert_entry(path_db,user_arg1)
	UsersManager.insert_entry(path_db,user_arg2)

	#search test
	users_list=UsersManager.select_Allentry(path_db)
	print(users_list)
	user_entry=UsersManager.select_ByName(path_db,'RPi1_node_0')
	print(user_entry)

	#update test
	update_arg1=['RPi1_node_0', 'Viewer', '0xaa09c6d65908e54bf695748812c51d8f2ceea0f5', '2018-11-8 18:39:42']
	UsersManager.update_entry(path_db,update_arg1)
	print(UsersManager.select_ByName(path_db,update_arg1[0]))

	#delete test
	#UsersManager.delete_ByName(path_db,user_arg1[0])
	print(UsersManager.select_ByName(path_db,user_arg1[0]))


if __name__ == '__main__': 
	test_user()

	pass


