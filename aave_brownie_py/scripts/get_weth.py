from scripts.helpful_scripts import get_account
from brownie import interface, config, network

def main():
    get_weth() 

def get_weth():
    """
    Mints WETH by depositing ETH to the WETHGateway contract
    Uses the interface (IWeth) to interact with the contract
    Once we have WETH we can interact with AAVE
    Since AAVE requires an ERC20 (hence we swap ETH for an ERC20 simulation of ETH (WETH))
    """
    account = get_account(id="eth_metamask")
    
    # not deploying any mocks so not doing get_contract
    weth = interface.IWeth(config['networks'][network.show_active()]['weth_token'])
    tx = weth.deposit({"from":account, "value":0.1 * 10 ** 18}) # 0.1 eth
    tx.wait(1)
    print(f"Received 0.1 WETH")
    return tx