import {useContractFunction, useEthers} from "@usedapp/core"
import { constants, utils } from "ethers"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/MockERC20.json"
import networkMapping from "../chain-info/deployments/map.json"
import {Contract} from "@ethersproject/contracts"
import { useEffect, useState } from "react"


export const useStakeTokens = (tokenAddress: string) => {
    // need to approve the tx
    // therefore need address, abi, chain ID
    const {chainId} = useEthers()
    const {abi} = TokenFarm
    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]['TokenFarm'][0] : constants.AddressZero

    const tokenFarmInterface = new utils.Interface(abi)
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)
    // now that we have the contract we can call the functions on it!!
    // first get the token contract as well
    const erc20ABI = ERC20.abi
    const erc20Interface = new utils.Interface(erc20ABI)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)

    // approve
    const {send: approveErc20Send, state: approveAndStakeErc20State} = 
    useContractFunction(
        erc20Contract, 
        "approve", 
        {transactionName: "Approve ERC20 transfer"}
    )
    const approveAndStake = (amount:string) => {
        setAmountToStake(amount)
        return approveErc20Send(tokenFarmAddress, amount)
    }
    // const [state, setState] = useState(approveAndStakeErc20State)

    // stake
    const {send: stakeSend, state: stakeState} = 
    useContractFunction(
        tokenFarmContract, 
        "stakeTokens", 
        {transactionName: "Stake Tokens",}
    )
    // how much we are going to stake
    const [amountToStake, setAmountToStake] = useState("0")

    // useEffect
    // allows us to do something if some variable has changed
    useEffect(() => {
        if(approveAndStakeErc20State.status === "Success") {
            // stake function
            stakeSend(amountToStake, tokenAddress)
        }
    }, [approveAndStakeErc20State, tokenAddress, amountToStake]) // this is the array of things we want to track, if anything changes useEffect is triggered in the function


    const [state, setState] = useState(approveAndStakeErc20State)
    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success"){
            setState(stakeState)
        } else {
            setState(approveAndStakeErc20State)
        }
    }, [approveAndStakeErc20State, stakeState])

    return {approveAndStake, state}
}