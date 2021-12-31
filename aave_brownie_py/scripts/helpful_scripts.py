from brownie import network, accounts, config

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']

def get_account(index=None, id=None):
    """
    If we pass an index to this function we will use accounts[index]
    otherwise we will use accounts.load("id")
    if working on local chain use account[0]
    this depends on what you specify when you run "brownie run scripts/deploy.py" if you add "--network ropsten" for example
    On LMT-Desktop (#1) we have an account id of "eth_metamask" with the account (public address) ending af29 - which is the main account for all chains
    I am using for testing
    I need to put this on LMT-Desktop-2 as well
    """
    
    # if working on local chain use account[0]
    # this depends on what you specify when you run "brownie run scripts/deploy.py" if you add "--network ropsten" for example
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        print("going with local")
        return accounts[0]
    else:
        print("live chain network")
        return accounts.add(config['wallets']['from_key'])