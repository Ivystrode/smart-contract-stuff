import time

from scripts import helpful_scripts
from brownie import Lottery, network, config, MockV3Aggregator

def deploy_lottery():
    # account = helpful_scripts.get_account(id="eth_metamask")
    account = helpful_scripts.get_account()
    net = network.show_active()
    print(f"=================NETWORK=================\n{net}\n========================================")
    lottery = Lottery.deploy(
        helpful_scripts.get_contract("eth_usd_price_feed").address,# constructor of lottery.sol "priceFeedAddress"
        helpful_scripts.get_contract("vrf_coordinator").address,# need to map this to what its mock needs to be ...
        helpful_scripts.get_contract("link_token").address, # the chainlink token...
        config['networks'][network.show_active()]['fee'], # get the preset ones in brownie-config
        config['networks'][network.show_active()]['keyhash'],
        {"from":account},
        publish_source=config['networks'][network.show_active()].get('verify', False) # get the verify key - but if this isnt set, set this to False
    )
    print(f"Lottery contract address: {Lottery[-1]}")
    return lottery # so we can use this in testing
    

def start_lottery():
    account = helpful_scripts.get_account()
    lottery = Lottery[-1] # get the most recent/existing Lottery contract
    starting_tx = lottery.startLottery({"from":account})
    # wait for a second so brownie doesn't get confused by things happening too fast - can SOMETIMES happen, if so just name the variable the above line
    starting_tx.wait(1)
    
    print("The lottery has started")
    
def enter_lottery():
    account = helpful_scripts.get_account()
    lottery = Lottery[-1]
    # need to send entrance fee
    value = lottery.getEntranceFee() + 100000000 # add a bit of wei just in case we're slightly under the $50 min fee
    tx = lottery.enter({"from":account, "value":value})
    tx.wait(1)
    print("Entered the lottery!")
    
def end_lottery():
    # need LINK token because this calls the requestRandomness function from chainlink!
    account = helpful_scripts.get_account()
    lottery = Lottery[-1]
    
    # fund the contract - because this will be fairly common let's make it in the helpful scripts
    tx = helpful_scripts.fund_with_link(lottery.address)
    tx.wait(1)
    # end the lottery
    ending_transaction = lottery.endLottery({"from":account})
    ending_transaction.wait(1)
    # this function makes a request to a chainlink node
    # which responds to the fulfilRandomness function
    # we have to wait for this to finish
    # we could do a time.sleep(60)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the winner!!")
    # this won't work on a local (ganache) chain because there is no chainlink node to call...

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
    
    # the address is to get price feed contract address, on local sim chain or real chain
    # publish means publish and verify (must have api token as env var)
    
    # if we are on a persistent network like ropsten use that address (0x9326BFA02ADD2366b30bacB125260Af641031331)
    # this is stored in the config file under "ropsten" which we access like this:
    # if network.show_active() not in helpful_scripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    #     print(f"Active network (live): {network.show_active()}")
        
    # # if we are on a local sim chain we have to "mock" our own price feed like this:
    # else:
    #     helpful_scripts.deploy_mocks()
    #     price_feed_address = MockV3Aggregator[-1].address # use the most recently deployed aggregator
