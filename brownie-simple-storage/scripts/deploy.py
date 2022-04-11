from brownie import accounts, config, SimpleStorage


def deploy_simple_storage():
    account = accounts[0]
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
        25,
        {
            "from": account,
        },
    )
    tranaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def main():
    deploy_simple_storage()
