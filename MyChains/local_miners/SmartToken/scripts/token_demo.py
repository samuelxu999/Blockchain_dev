from web3 import Web3, HTTPProvider, IPCProvider
import json, datetime, time
import sys
import argparse

class MockSmartToken(object):
    def __init__(self, http_provider, contract_addr, contract_config):
        # configuration initialization
        self.web3 = Web3(HTTPProvider(http_provider))
        self.contract_address = Web3.toChecksumAddress(contract_addr)
        self.contract_config = json.load(open(contract_config))

        # new contract object
        self.contract = self.web3.eth.contract(address=self.contract_address, 
                                            abi=self.contract_config['abi'])

    ## return accounts address
    def getAccounts(self):
        return self.web3.eth.accounts
    
    ##  return balance of account  
    def getBalance(self, account_addr = ''):
        if(account_addr == ''):
            checksumAddr = self.web3.eth.coinbase
        else:
            checksumAddr = Web3.toChecksumAddress(account_addr)
        return self.web3.fromWei(self.web3.eth.getBalance(checksumAddr), 'ether')

    ## query value from a token
    def query_Token(self, tokenId):
        #@Change account address to EIP checksum format
        checksumAddr = Web3.toChecksumAddress(tokenId)

        ## call getTokens()
        token_value = self.contract.functions.getTokens(checksumAddr).call({'from': self.web3.eth.coinbase})
        print("Token_id:{}  value:{}".format(checksumAddr, token_value))

    ## deposit value to a token
    def deposit_Token(self, tokenId, tokenValue):
        #@Change account address to EIP checksum format
        checksumAddr = Web3.toChecksumAddress(tokenId)

        ## send depositToken()
        tx_hash = self.contract.functions.depositToken(checksumAddr, tokenValue).transact({'from': self.web3.eth.coinbase})
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(receipt)

    ## withdraw value from a token
    def withdraw_Token(self, tokenId, tokenValue):
        #@Change account address to EIP checksum format
        checksumAddr = Web3.toChecksumAddress(tokenId)

        ## send withdrawToken()
        tx_hash = self.contract.functions.withdrawToken(checksumAddr, tokenValue).transact({'from': self.web3.eth.coinbase})
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(receipt)

    ## get address from json file, helper function
    @staticmethod
    def getAddress(node_name):
        address_json = json.load(open('./addr_list.json'))
        return address_json[node_name]


def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run MockSmartToken."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-contract information, \
                        1-get_token, \
                        2-deposit_value, \
                        3-withdraw_value")

    parser.add_argument("--id", type=str, default="node1_0", 
                        help="input token id")

    parser.add_argument("--value", type=int, default="10", 
                        help="input token value")

    args = parser.parse_args(args=args)
    return args

if __name__ == "__main__":

    args = define_and_get_arguments()

    httpProvider = MockSmartToken.getAddress('HttpProvider')
    contractAddr = MockSmartToken.getAddress('SmartToken')
    contractConfig = '../build/contracts/SmartToken.json'

    ## new MockSmartToken instance
    myToken = MockSmartToken(httpProvider, contractAddr, contractConfig)

    ## switch test cases
    if(args.test_op==1):
        tokenId=MockSmartToken.getAddress(args.id)
        myToken.query_Token(tokenId)
    elif(args.test_op==2):
        tokenId=MockSmartToken.getAddress(args.id)
        myToken.deposit_Token(tokenId, args.value) 
    elif(args.test_op==3):
        tokenId=MockSmartToken.getAddress(args.id)
        myToken.withdraw_Token(tokenId, args.value)
    else:
        accounts = myToken.getAccounts()
        balance = myToken.getBalance(accounts[0])
        print("Host accounts: %s" %(accounts))
        print("coinbase balance:%d" %(balance))

