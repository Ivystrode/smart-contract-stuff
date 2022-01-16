import React from 'react';
import {DAppProvider, ChainId} from "@usedapp/core"
import {Header} from "./components/header"
import {Container} from "@material-ui/core"
import {Main} from "./components/main"

function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Kovan, ChainId.Rinkeby, 1337], // 1337 is ganache I think?
      notifications: {
        expirationPeriod: 1000, //ms, check every 1000ms
        checkInterval: 1000
      }
    }}>
      <Header></Header>
      <Container maxWidth="md">
      <Main />
      </Container>
      
      
    </DAppProvider>
  );
}

export default App;
