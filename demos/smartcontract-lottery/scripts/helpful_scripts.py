from pickletools import read_uint1
from brownie import accounts, network, config, MockV3Aggregator, Contract

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMAL = 8
STARTING_PRICE = 20000000000

def get_account(index=None, id=None):


    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"eth_usd_price_feed" : MockV3Aggregator}

def get_contract(contract_name):
    """
        This function will grab the contract addresses from the brownie config or return mocl contract

        args:
            contract_name(string)
        returns:
            brownie.network.contract.PrjectContract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)

    return contract

def deploy_mocks():
    print(f"The active network is: {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMAL, STARTING_PRICE,
                {"from": get_account()} )
        
    print("Mocks deployed!!")