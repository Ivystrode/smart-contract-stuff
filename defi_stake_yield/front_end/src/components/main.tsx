import {useEthers} from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import brownieConfig from "../brownie-config.json"
import {constants} from "ethers"


export const Main = () => {
    // show tokens from the wallet

    // get the address of different tokens
    // get the balance of the users wallet

    // send the brownie-config to src folder
    // send the build folder
    const {chainId} = useEthers()
    // helper config is just a small json file that maps network IDs to network names
    const networkName = chainId ? helperConfig[chainId] : "dev" // if we are connected to a chain id then use the helperconfig
    console.log(networkName)
    console.log(chainId)

    // we imported brownie config where we extract these pieces of info
    // note - the dapp token address is in te map.json file. But when on development chain we need to replace chainId with networkName because that
    // is what it is saved under in map.json for some reason, while other chains are saved under their chain ID...
    const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero // if the chain id exists then get the dapptokenaddress from the map.json
    const wethTokenAddress = chainId ? brownieConfig['networks'][networkName]['weth_token'] : constants.AddressZero
    const fauTokenAddress = chainId ? brownieConfig['networks'][networkName]['fau_token'] : constants.AddressZero

    console.log(dappTokenAddress)
    console.log(wethTokenAddress)
    console.log(fauTokenAddress)




    return <div>Main</div>
} 