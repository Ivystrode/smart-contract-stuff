NOTES

GANACHE
- Runs a virtual blockchain on the local machine
- Run as either sync'd CLI program with brownie, or in the GUI

BROWNIE
- Automates much of what would otherwise be done with lots of python code
- brownie-config.yaml - store wallet addresses and dependency mappings
- commands
    - brownie compile - compiles the contract (should appear in a "build" folder)
        - will be inside a folder named after the chain id of chain it is deployed on
    - brownie run [scriptname] --network [networkname ie ropsten] [functionname - optional]

INFURA
- Does what? Gives us some api token?

ETHERSCAN/VERIFICATION
- Make an account to get an API key to verify contracts
- To verify and publish a contract - we can do manually on etherscan...
    - But we then have to "flatten" the imports as "import "@chainlink/safemath" etc doesn't work on etherscan
    - Flattening is pasting the code of the import at the top of the same file as the contract/.sol file
- This can also be done in brownie - sign up (etherscan) and get an API key...
    - Put the API key in a .env file or env var
    - then when you deploy, set "publish_source = True" in deploy.py after the from account bit
    - Source code will be published on deployment and you get a verified check mark on etherscan
    - imports are also flattened
    - you can then even interact with the contract on the "write contract" tab
    - verifying can be buggy
- To make this work on a local simulated chain, do a similar thing to the "get account" function
- This is because when we call the price feed contract/function, we are calling to a specific contract on a chain - which won't be accessible on a local chain
    - The priceFeed address (the contract we call to get the price of eth etc) will need to be passed as a parameter to our contract's constructor function
    - This means that we can tell it if we are using a simulated test or real chain
    - In deploy script pass the contract address as an argument/parameter for the constructor function
    - Make a "test" folder in contracts folder where you will store mock contracts
    - Make your mock contracts in here to use when local/sim chain testing/dev (find & paste the code...)

-DEPLOY TO PERSISTENT GANACHE
    - Use GUI to create a chain
    - Keep it running & deploy locally - notice it now listens on localhost now spin up its own chain
    - In ganache settings make sure you are using port 8545 otherwise it won't see the chain
    - Brownie doesn't track this in the build/deployments directory (only live netowrks), needs to be told to do so:
        - Add a network to brownie (any evm blockchain!)
        - brownie networks add Ethereum ganache-local host=http://127.0.0.1:8545 chainid=5777
        - it will now appear in brownie networks list
        - Keep the ganache instance running!
        - Now can run brownie run scripts deploy.py --networks ganache-lcao
        - Be aware this will not show as "development" in show networks! Fixed by making a list of what counts as a "development" environment in helpful_scripts.py that is checked against in deploy.py
        - Now we need to have gas to deploy - make sure get_account checks if environment is a local/dev one also
            - Create ganache-local network in config file with verify set to False
    - If you close ganache you lose the chain...you can then delete the [chain id] folder to restart


MAINNET FORK
    - You can "deploy" to a fork of the mainnet. mainnet-form is recognised by brownie - add it to the networks in the config
    - Verify to False
    - eth-usd price feed you can use the mainnet contract address (https://docs.chain.link/docs/ethereum-addresses/ look under mainnet obviously)
    - No wait...call mainnet-fork mainnet-fork-dev (make sure to add this to helpful_scripts)
    - Then run: brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/lDYQgk_KF967ieR-SORs5WKdIKjWHFYX accounts=10 mnemonic=brownie port=8545
    - Have to set up as an app on alchemyapi.io (apparently less buggy than infura??)
