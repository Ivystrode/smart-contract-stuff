import {useEthers} from "@usedapp/core"
import {Button, makeStyles} from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
    container: {
        padding: theme.spacing(4),
        display: "flex",
        justifyContent: "flex-end",
        gap: theme.spacing(1)
    }
}))

export const Header = () => {
    const classes = useStyles()
    const {account, activateBrowserWallet, deactivate} = useEthers()

    const isConnected = account !== undefined // if the account == "undefined" we are NOT connected

    return (
        <div className={classes.container}>
            <div>
                {isConnected ? (
                <Button variant="contained" color="primary" onClick={deactivate}>
                    Disconnect
                </Button>   
                ) : ( // else is the colon
                    <Button variant="contained" color="primary" onClick={() => {activateBrowserWallet()}} >
                        Connect
                    </Button>
                )
            }
            </div>            
        </div>

    )
}