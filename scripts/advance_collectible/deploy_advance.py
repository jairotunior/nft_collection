from brownie import AdvancedCollectible, accounts, network, config

def main():
    dev_account = accounts.add(config['wallets']["from_key"])
    # accounts.from_mnemonic(config["wallets"]["from_mnemonic"])

    print(dev_account)
    print(network.show_active())