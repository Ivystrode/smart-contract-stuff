import {Token} from "../main"
import React, {useState} from "react"
import Box from "@material-ui/core/Box"
import { makeStyles } from "@material-ui/core"
import {TabContext, TabList, TabPanel} from "@material-ui/lab"
import {Tab} from "@material-ui/core"
import {WalletBalance} from "./WalletBalance"
import { StakeForm } from "./stakeForm"


interface YourWalletProps {
    supportedTokens: Array<Token>
}

const useStyles = makeStyles((theme) => ({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4)
    },
    box: {
        backgroundColor: "gray",
        borderRadius: "25px"
    },
    header: {
        color: "white"
    }
}))



// in order to show the tokens we need some info on what the supported tokens are
// so Main component will pass a variable to this
// this tells TS what the supported tokens looks like
export const YourWallet = ({supportedTokens} : YourWalletProps) => {
    // a state hook to select tokens
    // this creates one variable
    // its a way of saving state through renders of components
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    // whenever we change tab in the Box the selected token is different
    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue))
    }
    const classes = useStyles()
    return (
        <Box>
            <h1 className={classes.header}>Your Wallet</h1>
            <Box className={classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList onChange={handleChange} aria-label="stake form tabs">
                        {/* for each token make a tab in the tab list */}
                        {supportedTokens.map((token, index) => {
                            return (
                                <Tab label={token.name}
                                value={index.toString()}
                                key={index} />
                            )
                        })}    
                    </TabList>    
                    {supportedTokens.map((token, index) => {
                        return (
                            <TabPanel value={index.toString()} key={index}>
                                {/* get wallet balance and stake button */}
                                <div className={classes.tabContent}>
                                   <WalletBalance token={supportedTokens[selectedTokenIndex]}/> 
                                   <StakeForm token={supportedTokens[selectedTokenIndex]}/>
                                </div>
                                
                            </TabPanel>
                        )
                    })}
                </TabContext>        
            </Box>

        </Box>
    )
}