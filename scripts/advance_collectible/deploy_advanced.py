from brownie import AdvancedCollectible, accounts, network, config
from scripts.helpful_scripts import fund_advanced_collectible


def main():
    dev_account = accounts.add(config['wallets']["from_key"])
    # accounts.from_mnemonic(config["wallets"]["from_mnemonic"])

    #print(dev_account.balance())

    publish_source = False

    advance_collectible = AdvancedCollectible.deploy(
        config['networks'][network.show_active()]['vrf_coordinator'],
        config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['keyhash'],
        { "from": dev_account },
        publish_source=publish_source
    )

    fund_advanced_collectible(advance_collectible)

    return advance_collectible