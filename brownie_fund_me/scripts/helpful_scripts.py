from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 18 # most cryptos (all ERC20) use 18
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']

def get_account():
    # if working on local chain use account[0]
    # this depends on what you specify when you run "brownie run scripts/deploy.py" if you add "--network ropsten" for example
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        print("going with local")
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])
    
def deploy_mocks():
    print(f"The active network is: {network.show_active()}")
    print(f"Deploying mocks...")
    if len(MockV3Aggregator) <= 0: # only deploy if we haven't deployed one already
        mock_aggregator = MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()}) # toWei adds 18 decimals to 2000 to be compatible with ethereum
    print("Mocks deployed")