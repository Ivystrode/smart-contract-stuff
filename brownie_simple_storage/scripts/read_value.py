# this will read from the ropsten blockchain, from a contract we have deployed!

from brownie import SimpleStorage, accounts, config, network

def get_account():
    # if working on local chain use account[0]
    # this depends on what you specify when you run "brownie run scripts/deploy.py" if you add "--network ropsten" for example
    if (network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def read_contract():
    simple_storage = SimpleStorage[-1] # if you do 0 you always pick the first deployment - -1 means you pick the most recent deployment!
    
    #ABI        } brownie knows both of these already - in the deployments folder, under the chain id of the chain its deployed to, is the json file of the contract
    #Address    }
    
    print(simple_storage.retrieve())

def update_stored_value(): # dont know how to pass args to brownie run this function to choose what number...
    account = get_account()
    simple_storage = SimpleStorage[-1]
    transaction = simple_storage.store(420, {"from": account})

def main():
    read_contract()