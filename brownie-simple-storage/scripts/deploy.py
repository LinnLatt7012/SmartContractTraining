from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("myaccount")
    # account = accounts.add(config["wallets"]["from_key"])
    simple_storage = SimpleStorage.deploy(
        {
            "from": account,
        }
    )
    stored_value = simple_storage.retrieve()
    print(stored_value)
    tranaction = simple_storage.store(
        8,
        {
            "from": account,
        },
    )
    tranaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
