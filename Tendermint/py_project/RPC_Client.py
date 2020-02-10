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
    def abci_query(tx_data=''):            
        headers = {'Content-Type' : 'application/json'}
        api_url='http://localhost:26657/abci_query'

        payload_str = "data="+ '"' + tx_data + '"'

        response = requests.get(api_url, params=payload_str, headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response

    '''
    Send transaction to network
    curl -s 'localhost:26657/broadcast_tx_commit?tx="sam"'
    '''
    @staticmethod
    def broadcast_tx_commit(tx_data=''):          
        headers = {'Content-Type' : 'application/json'}
        api_url='http://localhost:26657/broadcast_tx_commit'

        payload_str = "tx="+ '"' + tx_data + '"'

        response = requests.post(api_url, params=payload_str, headers=headers)
        
        #get response json
        json_response = response.json()      

        return json_response
    

if __name__ == "__main__":
    print(PRC_Client.abci_info())
    print(PRC_Client.abci_query("samuel123"))
    print(PRC_Client.broadcast_tx_commit("samuel123"))
    pass
