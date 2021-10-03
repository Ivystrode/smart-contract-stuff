1. Users can enter the lottery with eth based on a usd fee
2. An admin will choose when the lottery is over
3. Lottery will select a random winner

How to test this

1. 'mainnet-fork'
    - brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/1Amkjmd_e5uDAVqCg9Clplqmuj5Y5NA0 accounts=10 mnemonic=brownie port=8545
    - after networks delete mainnet-fork (to delete brownie defaults)
2. 'development with mocks'
3. 'testnet'