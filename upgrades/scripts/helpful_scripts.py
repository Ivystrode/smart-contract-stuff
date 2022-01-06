from brownie import network, accounts, config
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development','ganache-local']
DECIMALS = 18 # most cryptos (all ERC20) use 18
INITIAL_VALUE = 200000000000
STARTING_PRICE = 200000000000
OPENSEA_URL = 'https://testnets.opensea.io/assets/{}/{}'
BREED_MAPPING = {0: "PUG",
                 1: "SHIBA_INU",
                 2: "ST_BERNARD"}

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
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        print("going with local")
        return accounts[0]
    else:
        print("live chain network")
        return accounts.add(config['wallets']['from_key'])
    
def encode_function_data(initializer=None, *args):
    """
    Initializer = box.store, 1
    If there are no args we get an error so we fix that with the if args == 0 bit
    -- pip install eth_utils btw
    
    Official notes: 
    Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x") # if its blank just return an empty hex string and the contract knows there are no arguments
    return initializer.encode_input(*args) # encode it into bytes so our smart contracts can understand it and know what function to call

def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    """
    If you are using a proxy admin contract, run the upgrade from that
    
    If you are not (ie you or another wallet is authorised to upgrade), run the upgrade from the proxy directly
    then if you want to use an initializer function call upgradeToAndCall to call the initializer
    Otherwise just run upgradeTo with the proxy contract
    """
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(proxy.address, 
                                                              new_implementation_address,
                                                              encoded_function_call,
                                                              {"from":account})
        else:
            transaction = proxy_admin_contract.upgrade(proxy.address, new_implementation_address, {"from":account})
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(new_implementation_address, encoded_function_call, {"from":account})
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from":account})
    
    return transaction