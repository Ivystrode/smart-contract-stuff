# to work with addresses:
from brownie import accounts, config, SimpleStorage


def deploy_simple_storage():
    # account = account[0] # the first account ganache makes (only works with ganache)
    # print(account)0x24165194fb2598d7e6a275b877fa69a4de4e7107371b4362f2fcb37ab0e03905
    
    # add an account wth brownie accounts new [name]
    # account = accounts.load("ben") # we made an account called ben
    # print(account)
    # you can use the private key of a real account to do this
    
    # never make real private keys (for real money) in env vars, only for test accounts
    #BUT to use env vars:
    # make a brownie-config.yaml file as shown (make sure to import is)
    # account = accounts.add(config['wallets']['from_key'])
    # print(account)
    
    #but for now we want to just use the first ganache account
    account = accounts[0]
    
    #deploy contract to a chain - much quicker than manually with web3.py
    simple_storage = SimpleStorage.deploy({"from":account})
    
    print(simple_storage)
    
    # interacting with our smart contract
    stored_value = simple_storage.retrieve() # one of the functions in the contract
    print("stored value:")
    print(stored_value)
    
    transaction = simple_storage.store(6969, {"from":account})
    transaction.wait(1) # wait for 1 block
    print("updated value")
    stored_value = simple_storage.retrieve()
    print(stored_value)


def main():
    deploy_simple_storage()
