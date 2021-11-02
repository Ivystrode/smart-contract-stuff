from brownie import network, accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, Contract
from web3 import Web3

DECIMALS = 18 # most cryptos (all ERC20) use 18
INITIAL_VALUE = 200000000000
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']

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



# MOCK CONTRACT MAPPINGS:
# we have to map the contract type to a name
# anytime we see ["eth_usd_price_feed"] we know its a mockv3aggregator - we need to deploy a mock
contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
                    "vrf_coordinator": VRFCoordinatorMock,
                    "link_token": LinkToken}
    
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
    
    # check if we even need to deploy a mock - if we are on a local chain
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0: #eg if MockV3Aggregator.length is 0 ie none are deployed on the local chain yet
            deploy_mocks() 
            
        contract = contract_type[-1] # get the latest of that contract (eg MockV3Aggregator[-1]) - if we deployed above then it will be that one
    # for deploying to a testnet:
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address & ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type._abi) # allows us to get a ctract from its abi and address
    return contract
            
    
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    """
    If we are on a local chain we don't have access to oracles/price feeds
    Therefore we need to deploy them to the local chain so our contract
    will work in local testing
    """
    
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from":account})
    print("Deploy mock")
    