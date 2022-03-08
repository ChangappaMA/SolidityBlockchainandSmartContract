from brownie import accounts, config, network, MockV3Aggregator
from dotenv import load_dotenv

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMAL = 8
STARTING_PRICE = 20000000000

load_dotenv()

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is: {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMAL, STARTING_PRICE,
                {"from": get_account()} )
        
    print("Mocks deployed!!")