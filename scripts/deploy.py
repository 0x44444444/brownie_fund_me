from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # Adding 'publish_source = True' means it'll verify the contract on etherscan
    # Uses the ETHERSCAN_TOKEN environment variable
    # pass the priceFeed contract address to the constructor
    # fund_me = FundMe.deploy({"from": account}, publish_source=True)

    # We want to be able to change the address of the supposed price oracle depending on whether we're
    # on a local development network, or an actual persistent test net.

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # Deploy using the address of the oracle on Goerli
        # We query the brownie-config.yaml 'networks' section in which we've added the various address for each network
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        # publish_source = True

    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        # Deploy the mock oracle contract
    # print(f"The active network is {network.show_active()}")
    # print("Deploying Mocks...")
    # We want to check if we already deployed the mock
    # Brownie remembers what we've deployed already
    # MockV3Aggregator, as a contract container, is a list
    # If the list is 0 length in size, we didn't deploy anything yet
    # if len(MockV3Aggregator) <= 0:
    # mock_aggregator = MockV3Aggregator.deploy(
    #    18, Web3.toWei(2000, "ether"), {"from": account}
    # )
    #     MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": account})
    # mock_aggregator = MockV3Aggregator[0]
    # price_feed_address = mock_aggregator.address
    # An index of -1 just means the most recently deployed version of this contract
    # price_feed_address = MockV3Aggregator[-1].address
    # print("Mocks deployed")
    # publish_source = False

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
