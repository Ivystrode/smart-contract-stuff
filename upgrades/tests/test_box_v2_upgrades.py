from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract, exceptions
import pytest

def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from":account})
    proxy_admin = ProxyAdmin.deploy({"from":account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address,
                                               proxy_admin.address,
                                               box_encoded_initializer_function,
                                               {"from":account, "gas_limit":1000000})
    
    # deploy BoxV2                                               
    box_v2 = BoxV2.deploy({"from":account})
    
    # slap the ABI of BoxV2 onto the proxy address
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        # this test will pass if it DOES raise this error, since we haven't upgraded yet
        proxy_box.increment({"from":account})
        
    # upgrade the contract and test we now have the increment function
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from":account})
    assert proxy_box.retrieve() == 1