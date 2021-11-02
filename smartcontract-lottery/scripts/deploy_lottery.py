from scripts.helpful_scripts import get_account, get_contract
from brownie import Lottery, network, config

def deploy_lottery():
    account = get_account(id="ropsten_2_account")
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,# constructor of lottery.sol "priceFeedAddress"
        get_contract("vrf_coordinator").address,# need to map this to what its mock needs to be ...
        get_contract("link_token").address, # the chainlink token...
        config['networks'][network.show_active()]['fee'], # get the preset ones in brownie-config
        config['networks'][network.show_active()]['keyhash'],
        {"from":account},
        publich_source=config['networks'][network.show_active()].get('verify', False) # get the verify key - but if this isnt set, set this to False
    )
    print("Deployed the lottery smart contract!!!")

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
