from brownie import network, accounts, config, VRFCoordinatorMock, MockV3Aggregator, MockOracle, LinkToken, Contract, MockDAI, MockWETH

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']
DECIMALS = 18 # most cryptos (all ERC20) use 18
INITIAL_VALUE = 200000000000
INITIAL_PRICE_FEED_VALUE = 2000000000000000000000
STARTING_PRICE = 200000000000
OPENSEA_URL = 'https://testnets.opensea.io/assets/{}/{}'
BREED_MAPPING = {0: "PUG",
                 1: "SHIBA_INU",
                 2: "ST_BERNARD"}

# MOCK CONTRACT MAPPINGS:
# we have to map the contract type to a name
# anytime we see ["eth_usd_price_feed"] we know its a mockv3aggregator - we need to deploy a mock
contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
                    "dai_usd_price_feed": MockV3Aggregator,
                    "fau_token": MockDAI,
                    "weth_token": MockWETH}

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
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])
    

    
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
    print(f"Get contract - checking {contract_type}")
    
    # check if we even need to deploy a mock - if we are on a local chain
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Looking on the local chain...")
        if len(contract_type) <= 0: #eg if MockV3Aggregator.length is 0 ie none are deployed on the local chain yet
            print(f"==={contract_type} not deployed - deploying===")
            deploy_mocks() 
        else:
            print("Contract already deployed")
            
        contract = contract_type[-1] # get the latest of that contract (eg MockV3Aggregator[-1]) - if we deployed above then it will be that one
    # for deploying to a testnet:
    else:
        print("Checking network chain...")
        contract_address = config["networks"][network.show_active()][contract_name]
        # address & ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi) # allows us to get a ctract from its abi and address
        print("Contract found on network chain")
    return contract
            
    
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_PRICE_FEED_VALUE):
    """
    If we are on a local chain we don't have access to oracles/price feeds
    Therefore we need to deploy them to the local chain so our contract
    will work in local testing
    """
    print("===deploying ALL mocks===")
    account = get_account()
    link_token = LinkToken.deploy({"from":account})
    print(f"Link token deployed to {link_token.address}")
    weth_token = MockWETH.deploy({"from":account})
    print(f"WETH token deployed to {weth_token.address}")
    dai_token = MockDAI.deploy({"from":account})
    print(f"DAI token deployed to {dai_token.address}")
    mock_price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from":account})
    print(f"Mock V3 Aggregator deployed to {mock_price_feed.address}")
    print("Deployed mocks")
    
def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): # 0.1 LINK?
    account = account if account else get_account() # if a parameter was passed
    link_token = link_token if link_token else get_contract("link_token") # again if the parameter was specified, otherwise find it
    
    tx = link_token.transfer(contract_address, amount, {"from":account}) # either this or use interfaces folder
    
    # if we dont have the whole contract we can just use an interface to interact with the contract
    # find the interface and paste it in as a file to interfaces dir
    # then use it like so:
    # link_token_contract = interfaces.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from":account})
    
    # so if we have the abi we can compile it and then use it using contract.from_abi
    # if not we can just use the interface...
    
    tx.wait(1)
    
    print("Funded contract")
    return tx

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]
