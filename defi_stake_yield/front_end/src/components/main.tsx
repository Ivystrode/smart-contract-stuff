import {useEthers} from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import brownieConfig from "../brownie-config.json"
import {constants} from "ethers"
import dapp from "../dapp.png"
import eth from "../eth.png"
import dai from "../dai.png"
import { YourWallet } from "./yourWallet/yourWallet"
import { makeStyles } from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)
    }
}))

// here we create "Token", which is a new "type"
// later on we fill "supportedTokens" with a list of these "types"
// and tell yourWallet.tsx what the tokens our platform supports are
// by passing it as a parameter from this component
export type Token = {
    image: string
    address: string
    name: string 
}


export const Main = () => {
    const classes = useStyles()
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

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "DAPP"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dai,
            address: fauTokenAddress,
            name: "DAI"
        }
    ]

    console.log(supportedTokens)




    return (<>
        <h2 className={classes.title}>Dapp Token App</h2>
        <YourWallet supportedTokens={supportedTokens}/>
        </>
    )
} 