from brownie import FundMe, network, config
from scripts.helpful_scripts import get_account
from dotenv import load_dotenv

load_dotenv()

def deploy_fund_me():
    account = get_account()
    #pass the price feed address to the fundme contract

    #check the network and assign the price feed address
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]

    fund_me = FundMe.deploy(price_feed_address,
        {"from": account}, publish_source=True)
    print(f"Contract deplyed to {fund_me.address}")


def main():
    deploy_fund_me()