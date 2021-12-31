from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import config, network, interface
from web3 import Web3

# just to keep things standard for now
amount = Web3.toWei(0.1, "ether")

def main():
    account = get_account()
    erc20_address = config['networks'][network.show_active()]['weth_token']  # weth is an erc20
    
    # if on local mainnet-fork we need to get some weth
    # if we're on a real/test network we should already have some in our account so don't need to
    if network.show_active() in ['mainnet-fork']:
        get_weth()
        
    lending_pool = get_lending_pool() # get the contract...
    
    # APPROVE THE CONTRACT FUNCTIONS TO OPERATE ON OUR TOKENS
    # approve sending the erc20:
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    
    # DEPOSIT FUNDS
    # now that it's approved we can use the lending pool deposit method on our tokens
    # function deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode) - referral code is deprecated, just put 0
    print(f"Depositing {amount}")
    tx = lending_pool.deposit(erc20_address, amount, account.address, 0, {"from": account})
    tx.wait(1)
    print(f"Deposited {amount}")
    
    # BORROW
    # figure out how much we can borrow
    # function getUserAccountData(address user)
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    
def get_borrowable_data(lending_pool, account):
    """
    Get the summary of the account ie health factor, total debt, available borrows, liquidation threshold
    """
    (total_collateral_eth, 
     total_debt_eth, 
     available_borrow_eth, 
     current_liquidation_threshold, 
     ltv, #loan to value
     health_factor) = lending_pool.getUserAccountData(account.address) # view function so we don't need to spend any gas
    
    # these are all sent as Wei so we want to convert them to be more readable
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    
    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrow_eth} worth of ETH")
    
    # amount you can borrow is always less than amount you deposit
    # this is because of the liquidation threshold
    # these are outlined in docs.aave.com/risk/asset-risk/risk-parameters
    # ethereum has an 80% loan to value - meaning you can only borrow up to 80% of the assets deposited
    # it has an 85% liquidation threshold - if you borrow more than 85% of your assets worth you get liquidated
    
    return (float(available_borrow_eth), float(total_debt_eth))
    
def get_lending_pool():
    """
    Get the contract address of the lending_pool
    This can change, so we use the AddressProvider - getLendingPool() function
    We're going to use an interface instead of writing the abi and address here
    """
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config['networks'][network.show_active()]['lending_pool_addresses_provider']
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    
    #ABI - get the interface for lending pool instead (from aave docs)
    #address - got that above
    # when we run brownie compile the interface/s compile down to the ABI so we can work with them
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def approve_erc20(amount, spender, erc20_address, account):
    """
    Approves the lending_pool contract to use our ERC20 token (WETH)
    https://medium.com/ethex-market/erc20-approve-allow-explained-88d6de921ce9
    Need ABI and address of the token contract
    We will just get the interface and paste it to IERC20.sol
    """
    print("Approving ERC20 token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from":account})
    tx.wait(1)
    print("ERC20 Approved")
    return tx