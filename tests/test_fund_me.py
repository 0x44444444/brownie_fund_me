from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    # Ridiculously, we have to add 1 to the value sent to get this to work
    # Is there a rounding error somewhere?
    entrance_fee = fund_me.getEntranceFee() + 1
    print(f"The entrance fee is {entrance_fee} wei")
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    print("here")
    tx.wait(1)
    assert fund_me.addToAmount(account.address) == entrance_fee
    print("here2")
    tx2 = fund_me.withdraw({"from": account})
    print("here3")
    tx2.wait(1)
    print("here4")
    assert fund_me.addToAmount(account.address) == 0
    print("here5")


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # If we're on a production network, we're not going to test this
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    # Random account
    # bad_actor = accounts.add()
    bad_actor = accounts[1]
    print(f"The address of accounts[1] is {bad_actor.address}")
    # This is a condensed try/catch
    # Basically says, all is well if we raise this exception from the following block of code
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw(
            # This required some alteration from the tutorial - explicity allowing a revert, and ignoring gas estimation
            {"from": bad_actor, "gas_limit": 1200000, "allow_revert": True}
        )
