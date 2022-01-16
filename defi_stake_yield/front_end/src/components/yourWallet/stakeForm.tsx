import { useEthers, useTokenBalance, useNotifications } from "@usedapp/core";
import { Token } from "../main";
import {formatUnits} from "@ethersproject/units"
import {Button, Input, CircularProgress, Snackbar} from "@material-ui/core"
import Alert from "@material-ui/lab/Alert"
import React, { useEffect, useState } from "react";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import {utils} from "ethers"

export interface StakeFormProps {
    token: Token
}

export const StakeForm = ({token}: StakeFormProps) => {
    const{address:tokenAddress, name} = token 
    const {account} = useEthers()
    const tokenBalance = useTokenBalance(tokenAddress, account)
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)): 0
    const {notifications} = useNotifications()

    // a state hook to track the amount in the input box
    const [amount, setAmount] = useState<number | string | Array<number | string>>(0)
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value)
        setAmount(newAmount)
        console.log(newAmount)
    }

    const {approveAndStake, state: approveAndStakeErc20State} = useStakeTokens(tokenAddress)

    const handleStakeSubmit = () => {
        const amountAsWei= utils.parseEther(amount.toString())
        return approveAndStake(amountAsWei.toString())
    }



    // whether or not approve and stake are done
    const isMining = approveAndStakeErc20State.status === "Mining"
    // another hook to track approve erc20
    const [showErc20ApprovalSuccess, setShowErc20ApprovalSuccess] = useState(false)
    const [showStakeTokenSuccess, setShowStakeTokenSuccess] = useState(false)
    useEffect(()=> {
        if (notifications.filter(
            (notification) => 
            notification.type == "transactionSucceed" &&
            notification.transactionName === "Approve ERC20 transfer").length > 0 ){
                console.log("Approved")
                setShowErc20ApprovalSuccess(true)
                setShowStakeTokenSuccess(false)
            }
        if (notifications.filter(
            (notification) => 
                notification.type === "transactionSucceed" &&
                notification.transactionName === "Stake Tokens").length > 0) {
                    console.log("Tokens staked")
                    setShowErc20ApprovalSuccess(false)
                    setShowStakeTokenSuccess(true)
                }
    }, [notifications, showErc20ApprovalSuccess, showStakeTokenSuccess]) // if any notification changes/appears do something


    const handleCloseSnack = () => {
        setShowErc20ApprovalSuccess(false)
        setShowStakeTokenSuccess(false)
    }

    return (
        <>
        <div>
            <Input
            onChange={handleInputChange}/>
            <Button
            onClick={handleStakeSubmit}
            color="primary"
            size="large"
            disabled={isMining}>
                {isMining ? <CircularProgress size={26}/> : "Stake"}
            </Button>
        </div>

        <Snackbar open={showErc20ApprovalSuccess} autoHideDuration={5000} onClose={handleCloseSnack} >
            <Alert onClose={handleCloseSnack} severity="success">
                ERC20 token transfer approved, now approve the 2nd transaction
            </Alert>
        </Snackbar>

        <Snackbar open={showStakeTokenSuccess} autoHideDuration={5000} onClose={handleCloseSnack} >
            <Alert onClose={handleCloseSnack} severity="success">
                Tokens staked!
            </Alert>
        </Snackbar>
        </>
    )
}