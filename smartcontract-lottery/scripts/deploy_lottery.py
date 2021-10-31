from scripts.helpful_scripts import get_account, get_contract
from brownie import Lottery, network

def deploy_lottery():
    account = get_account(id="ropsten_2_account")
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed")
    )

def main():
    deploy_lottery()
    
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
