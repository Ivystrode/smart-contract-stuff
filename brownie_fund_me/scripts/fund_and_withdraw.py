from brownie import FundMe
from scripts import helpful_scripts

def fund():
    fund_me = FundMe[-1]
    account = helpful_scripts.get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"The entrance fee is: {entrance_fee}")
    print("Funding...")
    fund_me.fund({"from":account, "value": entrance_fee})
    
def withdraw():
    fund_me = FundMe[-1]
    account = helpful_scripts.get_account()
    fund_me.withdraw({"from":account})
    
def main():
    fund()
    withdraw()