1. Users can enter the lottery with eth based on a usd fee
2. An admin will choose when the lottery is over
3. Lottery will select a random winner

How to test this

1. 'mainnet-fork' - run this on LMT DT2:
    - brownie networks delete mainnet-fork
    - brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/1Amkjmd_e5uDAVqCg9Clplqmuj5Y5NA0 accounts=10 mnemonic=brownie port=8545
    - add the alchemyapi connection
2. 'development with mocks'
3. 'testnet'

The setup

1. brownie init - starts new brownie project
2. add dependencies to brownie-config.yaml & remappings
3. brownie compile to test the sol file
4. delete brownie inbuilt internal mainnet fork - brownie networks delete mainnet-fork
5. using alchemy as our ethereum connection - create an app and get the API key
6. brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=[alchemyhttp] accounts=10 mnemonic=brownie port=8545
    -   Make sure to add account to brownie with brownie accounts new [name] [private_key]
7. test - write test script and run brownie test --network mainnet-fork

8. Using LINK oracles & services - for testnets we can acquire this from faucets, look at chainlink docs to find testnet ETH and LINK faucets
9. One such service is random number generation - the random number contract costs LINK to use!
10. This follows the Request and Receive cycle of getting data...TWO transactions take place. One is the request from the contract to the off chain server (chainlink node) rand generator, the other (receive) is the callback function of the caller contract. Just like how we made the oracle/caller contract in cryptozombies. Our callback function in this case is the fulfilling randomness function that the chainlink node calls to give the rnadom number to the contract...

11. Deploy - in scripts dir create a deploy.py file
12. Create an __init__.py in the scripts folder so python recognises it as an importable module
13. Create a helpful_scripts.py file to hold helpful scripts like get_account etc
14. Create .env file with all private keys and api keys in
15. in brownie-config.yaml add wallets: from_key: ${PRIVATE_KEY}

Testing on a testnet!
1. Do testing - see test dir - unit tests are usually done on local dev chain and integration tests on testnet
2. brownie test -k [functionname(if wanting to do one function)] --network [networkname]
3. I did this with ropsten - making sure the project id is in .env and that config points to the dotenv file - make sure it skips if network.show_active is local/development
4. Do some unit tests on local environment...se unit test file/folder
5. Deploying to testnet to test