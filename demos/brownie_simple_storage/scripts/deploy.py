from re import S
from brownie import accounts, SimpleStorage

def deploy_simple_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)

    updated = simple_storage.retrieve()
    print(updated)



def main():
    deploy_simple_storage()