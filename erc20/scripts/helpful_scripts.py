from brownie import network, accounts, config
from web3 import Web3

# DECIMALS = 18 # most cryptos (all ERC20) use 18
# INITIAL_VALUE = 200000000000
# STARTING_PRICE = 200000000000

# FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
# LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']

def get_account(index=None, id=None):
    """
    If we pass an index to this function we will use accounts[index]
    otherwise we will use accounts.load("id")
    if working on local chain use account[0]
    this depends on what you specify when you run "brownie run scripts/deploy.py" if you add "--network ropsten" for example
    On LMT-Desktop (#1) we have an account id of "ben" with the account (public address) ending af29 - which is the main account for all chains
    I am using for testing
    I need to put this on LMT-Desktop-2 as well
    """
    
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    else:
        return accounts[0]