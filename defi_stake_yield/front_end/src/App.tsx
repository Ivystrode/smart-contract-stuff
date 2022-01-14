import React from 'react';
import {DAppProvider, ChainId} from "@usedapp/core"
import {Header} from "./components/header"
import {Container} from "@material-ui/core"
import {Main} from "./components/main"

function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Kovan, ChainId.Rinkeby, 1337] // 1337 is ganache I think?
    }}>
      <Header></Header>
      <Container maxWidth="md">
        <div>Ji</div>
      </Container>
      <Main />
      
    </DAppProvider>
  );
}

export default App;
