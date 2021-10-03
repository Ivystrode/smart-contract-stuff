# pylance: disable=wildcard-import

from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts import helpful_scripts
from web3 import Web3


def deploy_fund_me():
    print("get account")
    # get account, simulated or real
    account = helpful_scripts.get_account()
    
    # the address is to get price feed contract address, on local sim chain or real chain
    # publish means publish and verify (must have api token as env var)
    
    # if we are on a persistent network like ropsten use that address (0x9326BFA02ADD2366b30bacB125260Af641031331)
    # this is stored in the config file under "ropsten" which we access like this:
    if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
        print(f"Active network (live): {network.show_active()}")
        
    # if we are on a local sim chain we have to "mock" our own price feed like this:
    else:
        helpful_scripts.deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address # use the most recently deployed aggregator

    
    fund_me = FundMe.deploy(price_feed_address, {"from":account}, publish_source=config['networks'][network.show_active()].get("verify")) 
    print(f"Contract deployed to {fund_me.address}")
    return fund_me
    

def main():
    deploy_fund_me()