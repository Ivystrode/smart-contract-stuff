from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import network, Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract

def main():
    account = get_account()
    print(f"deploying to {network.show_active()}")
    box = Box.deploy({"from":account}, publish_source=True)
    print(box.retrieve())
    
    # this will error out as Box has no "increment" function
    # print(box.increment())
    
    # so we hook it up to a proxy...
    # we need a proxy admin, this can be a wallet (ie YOU), multisig wallet for example to be more decentralised/safer
    # https://help.gnosis-safe.io/en/articles/3876461-create-a-safe
    proxy_admin = ProxyAdmin.deploy({"from":account}, publish_source=True)
    
    # encode the initializer function
    # initializer = box.store, 1 # store is the function to call and 1 is the parameter, uncomment this and use as an arg below to deploy with an initializer
    box_encoded_initializer_function = encode_function_data() # if we add args to this we are telling it to use an initializer
    
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address, # we COULD just say this is us, btu we're using the proxy admin
        box_encoded_initializer_function,
        {"from":account, "gas_limit":1000000}#, # proxies sometimes struggle to figure out the gas limit
        # publish_source=True # something goes wrong when we try and verify this contract and the script fails to complete...
    )
    print(f"Proxy deployed to {proxy}, you ca now upgrade to BoxV2")

    # we want to call functions through the proxies, because that's where we can change things rather than the original contract
    # we assign the proxy address the ABI of the Box contract
    # then the proxy delegates all of its calls to the Box contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    
    # so we can call functions like this
    print("Calling function via proxy")
    proxy_box.store(6779, {"from":account})
    print(proxy_box.retrieve())
    
    # the proxy_box will always be/point to the most recent box contract
    
    # upgrade to V2 of the contract
    print("Deploying Box V2")
    box_v2 = BoxV2.deploy({"from":account}, publish_source=True)
    upgrade_transaction = upgrade(account, 
                                  proxy, 
                                  box_v2.address, 
                                  proxy_admin_contract = proxy_admin, # we dont have an initializer
                                  )
    upgrade_transaction.wait(1)
    
    print("Proxy has been upgraded, testing")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from":account})
    print(proxy_box.retrieve())