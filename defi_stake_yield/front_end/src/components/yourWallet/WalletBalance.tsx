import { useEthers, useTokenBalance } from "@usedapp/core"
import {Token} from "../main"
import {formatUnits} from "@ethersproject/units"
import {BalanceMsg} from "../BalanceMsg"

export interface WalletBalanceProps {
    token: Token
}

export const WalletBalance = ({token}: WalletBalanceProps)=> {
    const {image, address, name} = token 
    const {account} = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    // change it from a fuckhuge number by getting rid of excess decimal places
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    console.log("Balance:")
    console.log(formattedTokenBalance?.toString())
    return (<BalanceMsg 
        amount={formattedTokenBalance} 
        label={`Your unstaked ${name} balance`}
        tokenImgSrc={image}
        />)
}