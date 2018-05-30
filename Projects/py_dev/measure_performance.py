#!/usr/bin/env python

'''
========================
meas_perform module
========================
Created on Nov.13, 2017
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide performance measure utilities.
'''
import matplotlib
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

class ExecTime(object):
	'''
	merge execution time from client and server
	'''
	@staticmethod
	def merge_exec_time(client_log, server_log):
		f_client = open(client_log, 'r')
		ls_client=f_client.readlines()
		#close file
		f_client.close()
		
		f_server = open(server_log, 'r')
		ls_server=f_server.readlines()
		#close file
		f_server.close()
		
		line_len=len(ls_client)
		
		exec_time_data=[]
		
		for i in range(line_len):
			ls_client[i]=ls_client[i].replace('\n','')
			ls_server[i]=ls_server[i].replace('\n','')
			if(ls_client[i]=='' or ls_server[i]==''):
				continue
			tmp_str=ls_server[i] +" " + ls_client[i]
			exec_time_data.append(tmp_str.split())
		
		return exec_time_data
	
	'''
	merge data from a and b
	'''
	@staticmethod
	def merge_data(a_log, b_log):
		f_a = open(a_log, 'r')
		ls_a=f_a.readlines()
		#close file
		f_a.close()
		
	
		f_b = open(b_log, 'r')
		ls_b=f_b.readlines()
		#close file
		f_b.close()
		
		line_len=len(ls_a)
		
		merged_data=[]
		for i in range(line_len):
			ls_a[i]=ls_a[i].replace('\n','')
			ls_b[i]=ls_b[i].replace('\n','')
			
			if(ls_a[i]=='' or ls_b[i]==''):
				continue
			tmp_str=ls_a[i] +" " + ls_b[i]
			merged_data.append(tmp_str.split())
		
		return merged_data
	
	'''
	merge data from multiple files
	'''
	@staticmethod
	def merge_files(file_list):
		file_count=len(file_list)
		
		#read data from files
		data_list=[]
		for i in range(file_count):
			#print(file_list[i])
			fname=open(file_list[i], 'r')
			data=fname.readlines()
			fname.close()
			data_list.append(data)
			
		#get row size based on branchmark dataset
		data_size=len(data_list[0])
		#print(str(file_count)+" "+ str(data_size))
		
		#merge data to single dataset
		merged_data=[]
		for row in range(data_size):
			row_data=[]
			for col in range(file_count): 
				data_list[col][row]=data_list[col][row].replace('\n','')
				row_data.append(data_list[col][row])
			merged_data.append(row_data)

		return merged_data

	'''
	calculate execution time by using average
	'''
	@staticmethod
	def calc_exec_time(ls_exec_time):	
		ave_exec_time=[0.0, 0.0, 0.0, 0.0]
		
		for exec_time in ls_exec_time:
			for i in range(len(exec_time)):
				ave_exec_time[i]+=float(exec_time[i])
		
		for i in range(len(ls_exec_time[0])):
			ave_exec_time[i]=format(ave_exec_time[i]/len(ls_exec_time), '.3f')
		
		#print(ave_exec_time)
		return ave_exec_time

class VisualizeData(object):
	'''
	plot bar chart given ls_data
	'''
	@staticmethod
	def plot_bar(title_name, x_label, y_label, ls_data):
		x_pos = np.arange(len(x_label))
		
		#create bar list given ls_data
		Bar_list=plt.bar(x_pos, ls_data, align='center', alpha=0.5)
		
		#set color for each bar
		Bar_list[0].set_color('r')
		Bar_list[1].set_color('g')
		Bar_list[2].set_color('b')
		Bar_list[3].set_color('gray')
		
		#add value on bar
		ax=plt.axes()
		#ax.grid()
		for p in ax.patches:
			ax.annotate(str(p.get_height()), (p.get_x()+p.get_width()/4, p.get_height()+0.2))

		#plt.xticks(x_pos, x_label)
		plt.xticks(x_pos, [])
		plt.ylabel(y_label)
		plt.ylim(0, 400)
		plt.title(title_name)
		
		#handles, labels = ax.get_legend_handles_labels()
		ax.legend(Bar_list[::], x_label[::], loc='upper left')
		
		plt.show()
	
	'''
	plot groupbar chart given ls_data
	'''
	@staticmethod
	def plot_groupbar(xtick_label, y_label, legend_label, ls_data):
		
		N = len(xtick_label)
		
		ind = np.arange(N)  # the x locations for the groups
		width = 0.30       	# the width of the bars
		
		#generate bar axis object
		fig, ax = plt.subplots()
		
		blend_exec_time = ls_data[0]
		rects_blend = ax.bar(ind, blend_exec_time, width, color='g')
		
		rbac_exec_time = ls_data[1]	
		rects_rbac = ax.bar(ind + width, rbac_exec_time, width, color='r')
		
		abac_exec_time = ls_data[2]			
		rects_abac = ax.bar(ind + 2*width, abac_exec_time, width, color='b')
		
		# add some text for labels, title and axes ticks
		ax.set_ylabel(y_label)
		#ax.set_title('Execution time by group', fontsize=18)
		ax.set_xticks(ind + width)
		ax.set_xticklabels(xtick_label)
		plt.ylim(0, 280)
		
		ax.legend((rects_blend[0], rects_rbac[0], rects_abac[0]), legend_label, loc='upper left', fontsize=14)
		
		VisualizeData.autolabel(rects_blend, ax)
		VisualizeData.autolabel(rects_rbac, ax)
		VisualizeData.autolabel(rects_abac, ax)
		
		plt.show()
		pass	
	
	@staticmethod
	def autolabel(rects, ax):
		"""
		Attach a text label above each bar displaying its height
		"""
		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2, (height+0.2),
			        '%.1f' % height,
			        ha='center', va='bottom', fontsize=12)

	'''
	plot lines chart given ls_data
	'''
	@staticmethod
	def plot_lines(x_label, y_label, ls_data):
		x=[]
		token_verify=[]
		access_verify=[]
		sign_verify=[]
		total_delay=[]
		
		#prepare data for plot
		plot_data=[]
		i=1
		for record in ls_data:
			x.append(i)
			token_verify.append(record[0])
			access_verify.append(record[1])
			sign_verify.append(record[2])
			total_delay.append(record[3])
			i+=1
		
		plot_data.append(token_verify)
		plot_data.append(access_verify)
		plot_data.append(sign_verify)
		plot_data.append(total_delay)
		
		
		plot_gird='22'
		#define figure
		plt.figure(plot_gird) 
		
		for i in range(len(plot_data)):
			plotnum=plot_gird+str(i+1)
			
			#-----------subplot-Speed-----------
			plt.subplot(plotnum)
			#labels
			plt.xlabel(x_label[i])
			plt.ylabel(y_label)
			
			#plot data
			#plt.plot(x, plot_data[i])
			plt.plot(x, plot_data[i], lw=1.0)
			#plt.suptitle(x_label[i])
		
		#plt.title(title_name)
		
		#plt.savefig("test.pdf")
		
		#show plot
		plt.show()
		
		
	'''
	plot multiple lines in single chart given ls_data
	'''
	@staticmethod
	def plot_Multilines(title_name, x_label, y_label, ls_data):
		x=[]
		token_verify=[]
		access_verify=[]
		sign_verify=[]
		total_delay=[]
		
		#prepare data for plot
		i=1
		for record in ls_data:
			x.append(i)
			token_verify.append(record[0])
			access_verify.append(record[1])
			sign_verify.append(record[2])
			total_delay.append(record[3])
			i+=1
		line_list=[]
		line_list.append(plt.plot(x, token_verify, lw=1.0, color='r'))
		line_list.append(plt.plot(x, access_verify, lw=1.0, color='g'))
		line_list.append(plt.plot(x, sign_verify, lw=1.0, color='b'))
		line_list.append(plt.plot(x, total_delay, lw=1.0, color='gray'))
		plt.xlabel('Run cycles')
		plt.ylabel(y_label)
		
		plt.title(title_name)
		
		plt.legend(x_label, loc='upper left')
		
		#show plot
		plt.show()
		
	'''
	plot multiple lines in single chart given ls_data
	'''
	@staticmethod
	def plot_CapVsNoCap(title_name, x_label, y_label, ls_data):
		x=[]
		NoCap_delay=[]
		Cap_delay=[]
		RBAC_delay=[]
		ABAC_delay=[]
		
		#prepare data for plot
		i=1
		for record in ls_data:
			x.append(i)
			NoCap_delay.append(record[0])
			Cap_delay.append(record[1])
			RBAC_delay.append(record[2])
			ABAC_delay.append(record[3])
			i+=1
			
		line_list=[]
		line_list.append(plt.plot(x, NoCap_delay, lw=1.0, color='gray'))
		line_list.append(plt.plot(x, Cap_delay, lw=1.0, color='g'))
		line_list.append(plt.plot(x, RBAC_delay, lw=1.0, color='r'))
		line_list.append(plt.plot(x, ABAC_delay, lw=1.0, color='b'))
		plt.xlabel('Run cycles')
		plt.ylabel(y_label)
		plt.title(title_name)
		plt.ylim(0, 250)
		plt.legend(x_label, loc='upper right')
		
		#show plot
		plt.show()

def plot_bar():
	exec_time_data=ExecTime.merge_exec_time('ABAC_contract/exec_time_client.log', 'ABAC_contract/exec_time_server.log')
	#print(exec_time_data)
	ave_exec_time=ExecTime.calc_exec_time(exec_time_data)
	
	obj_label=['Process token data', 'Token validation', 'Authorization validation', 'Total Delay']
	
	VisualizeData.plot_bar("", obj_label, 'Time (ms)', ave_exec_time)	
	
def plot_line():
	exec_time_data=ExecTime.merge_exec_time('Lan/exec_time_client.log', 'Lan/exec_time_server.log')
	obj_label=['Token verification', 'Access right verification', 'Issuer signature verification', 'Total Delay']
	VisualizeData.plot_lines(obj_label, 'Time (ms)', exec_time_data)
	
def plot_multilines():
	exec_time_data=ExecTime.merge_exec_time('Wlan/exec_time_client.log', 'Wlan/exec_time_server.log')
	obj_label=['Token verification', 'Access right verification', 'Issuer signature verification', 'Total Delay']
	VisualizeData.plot_Multilines("Multi-Cycles Time", obj_label, 'Time (ms)', exec_time_data)

def plot_lines():
	#exec_time_data=ExecTime.merge_data('BlendCapAC_optimized/exec_time_client.log', 'CapVsNoCap/exec_time_client_NoCap.log')
	file_list=['CapVsNoCap/exec_time_client_NoCap.log']
	file_list.append('BlendCapAC_optimized/exec_time_client.log')
	file_list.append('RBAC_optimized/exec_time_client.log')
	file_list.append('ABAC_optimized/exec_time_client.log')
	exec_time_data=ExecTime.merge_files(file_list)
	
	#print(exec_time_data)
	obj_label=['No Access Control', 'BlendCAC', 'RBAC', 'ABAC']
	VisualizeData.plot_CapVsNoCap("", obj_label, 'Time (ms)', exec_time_data)

def plot_groupbar():
	xtick_label=['Token processing', 'Token validation', 'Access validation', 'Total Delay']
	legend_label=['BlendCAC', 'RBAC', 'ABAC']
	
	#prepare data
	ls_exec_time=[]
	blend_exec_time=ExecTime.merge_exec_time('BlendCapAC_contract/exec_time_client.log', 'BlendCapAC_contract/exec_time_server.log')
	blend_ave_exec_time=ExecTime.calc_exec_time(blend_exec_time)
	
	rbac_exec_time=ExecTime.merge_exec_time('RBAC_contract/exec_time_client.log', 'RBAC_contract/exec_time_server.log')
	rbac_ave_exec_time=ExecTime.calc_exec_time(rbac_exec_time)
	
	abac_exec_time=ExecTime.merge_exec_time('ABAC_contract/exec_time_client.log', 'ABAC_contract/exec_time_server.log')
	abac_ave_exec_time=ExecTime.calc_exec_time(abac_exec_time)
	
	#append data to list
	ls_exec_time.append(blend_ave_exec_time)
	ls_exec_time.append(rbac_ave_exec_time)
	ls_exec_time.append(abac_ave_exec_time)

	VisualizeData.plot_groupbar(xtick_label,'Time (ms)', legend_label, ls_exec_time)
	
def plot_BlockTime():
		miners=[2,3,4,5,6,7]
		block_time=[16.07, 15.65, 13.58, 9.37, 7.73, 7.95]
		
		plt.plot(miners, block_time, lw=1.0, color='green')
		plt.xlabel('Miner count')
		plt.ylabel('Time (sec)')
		plt.title("Block Average Generated Time")
		plt.ylim(0, 20)
		for x,y in zip(miners, block_time): 
			plt.plot(x, y, "b^")
			plt.text(x-0.1, y+0.5, str(y))
		
		#show plot
		plt.show()

if __name__ == "__main__":
	matplotlib.rcParams.update({'font.size': 16})
	#plot_bar()
	#plot_line()
	#plot_multilines()
	#plot_lines()
	#plot_groupbar()
	plot_BlockTime()
	pass