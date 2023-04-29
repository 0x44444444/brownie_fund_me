from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    # Figure out if we're using a real network and need a private key, or whether just to use the first accounnt in ganache
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS) or (
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        # return brownie.accounts.add(brownie.config["wallets"]["from_key"])
        return accounts.load("development-bs-738")


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    # We want to check if we already deployed the mock
    # Brownie remembers what we've deployed already
    # MockV3Aggregator, as a contract container, is a list
    # If the list is 0 length in size, we didn't deploy anything yet
    if len(MockV3Aggregator) <= 0:
        # mock_aggregator = MockV3Aggregator.deploy(
        #    18, Web3.toWei(2000, "ether"), {"from": account}
        # )
        MockV3Aggregator.deploy(
            # DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
            DECIMALS,
            STARTING_PRICE,
            {"from": get_account()},
        )
        # mock_aggregator = MockV3Aggregator[0]
        # price_feed_address = mock_aggregator.address
        # An index of -1 just means the most recently deployed version of this contract

    print("Mocks deployed")
