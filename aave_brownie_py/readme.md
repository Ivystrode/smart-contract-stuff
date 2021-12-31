0. Swap our ETH for WETH
1. Deposit some ETH
2. Borrow some asset with the ETH collateral
    - Sell that borrowed asset? "Short selling"
3. Repay everything back

This will also work with paraswap, uniswap

***https://docs.aave.com/developers/***

**0. Swapping for WETH**
AAVE swaps ETH for WETH, an ERC20 representation of ETH, so it can be used with tokens
It does this using its WETHGateway contract:
Look it up by looking up the TO field in your transaction to AAVE/protocol, it should be called something like WETHGateway - this is what AAVE uses to get WETH. This may save some gas...

But you can get WETH yourself by looking up the Wrapper Ether contract (NOT the one just called "WETH") on etherscan [network]
CAREFUL to get the right one, it can be confusing (there is another contract called WETH, find the one called Wrapper Ether)
Depositing ETH to this contract mints WETH that you then get

For testing:

Integration test: Kovan
Unit tests: Mainnet-fork -- fork everything on the mainnet onto a local fork
Since we do not need to work with oracles we don't need to deploy any mocks, so we can just use the mainnet-fork. This will be just like working with actual mainnet.

The ganache CLI will fork mainnet for us
REFER BACK TO SEE HOW TO SET UP MAINNET FORK (root readme)

**1. DEPOSIT SOME (W)ETH**
