from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 18 # most cryptos (all ERC20) use 18
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']

def get_account(index=None, id=None):
    """
    If we pass an index to this function we will use accounts[index]
    otherwise we will use accounts.load("id")
    if working on local chain use account[0]
    this depends on what you specify when you run "brownie run scripts/deploy.py" if you add "--network ropsten" for example
    """
    
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    else:
        return accounts[0]

    
def deploy_mocks():
    """
    If we are on a local chain we don't have access to oracles/price feeds
    Therefore we need to deploy them to the local chain so our contract
    will work in local testing
    """
    
    print(f"The active network is: {network.show_active()}")
    print(f"Deploying mocks...")
    if len(MockV3Aggregator) <= 0: # only deploy if we haven't deployed one already
        mock_aggregator = MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()}) # toWei adds 18 decimals to 2000 to be compatible with ethereum
    print("Mocks deployed")
    
# we have to map the contract type to a name
# anytime we see ["eth_usd_price_feed"] we know its a mockv3aggregator - we need to deploy a mock
contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}
    
def get_contract(contract_name):
    """
    This function will get the contract addresses from the brownie-config
    if defined, otherwise it will deploy a mock version of that contract and 
    return that mock contract.
    Args: contract_name(string)
    Returns: Contract (a brownie.network.contract.ProjectContract: the most recently
    deployed version of this contract - ie MockV3Aggregator[-1])
    """
    contract_type = contract_to_mock[contract_name]