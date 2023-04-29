from brownie import FundMe
from scripts.helpful_scripts import get_account


def main():
    fund()
    withdraw()


def fund():
    # the most recently deployed version of the contract that Brownie knows about (see 'build' folder for persistent mappings)
    fund_me = FundMe[-1]
    account = get_account()

    price = fund_me.getPrice()
    print(f"The price returned is{price}")

    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"The current entrance fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})
