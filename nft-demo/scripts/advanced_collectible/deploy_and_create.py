from brownie import network, AdvancedCollectible, config
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_contract
from web3 import Web3


def deploy_and_create():
    """
    we want to use the deployed contracts if we are on a testnet
    otherwise we want to deploy some mocks and use those
    """
    account = get_account()
    
    advanced_collectible = AdvancedCollectible.deploy(get_contract("vrf_coordinator"), 
                                                      get_contract("link_token"),
                                                      config['networks'][network.show_active()]['keyhash'],
                                                      config['networks'][network.show_active()]['fee'],
                                                      {"from":account})
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from":account})
    creating_tx.wait(1)
    print("New token has been created")
    return advanced_collectible, creating_tx # so we can test for the request ID

def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")): # 0.1 LINK?
    account = account if account else get_account() # if a parameter was passed
    link_token = link_token if link_token else get_contract("link_token") # again if the parameter was specified, otherwise find it
    
    tx = link_token.transfer(contract_address, amount, {"from":account}) # either this or use interfaces folder
    
    tx.wait(1)

def main():
    deploy_and_create()