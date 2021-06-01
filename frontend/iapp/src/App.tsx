import React, { useEffect }  from 'react';
import TwitterUserSummary from './pages/TwitterUserSummary';
import SignIn from './pages/SignIn';
import Header from './layout/Header';
import SideBar from './layout/SideBar';
import { MuiThemeProvider } from '@material-ui/core/styles';
import { appTheme } from './theme/materialui';
import { userPool } from './aws/Cognito';
import './App.css';


function App() {

  const [signedIn, setSignedIn] = React.useState<boolean|null>(null);
  const [signedInUserName, setSignedInUserName] = React.useState<string>("");

  useEffect(() => {
    const cognitoUser = userPool.getCurrentUser()
    if (cognitoUser) {  // Already signed in.
      setSignedIn(true);
      setSignedInUserName(cognitoUser.getUsername());
      console.log('signed in');
    } else {
      setSignedIn(false);
      setSignedInUserName("");
      console.log('no user signing in');
    }
  }, [])

  const signedInContents = () => {
    return (
      <div className="authorizedMode">
        <h3>You're now signed in as {signedInUserName}.</h3>
        <TwitterUserSummary />
      </div>
    )
  }

  const signedOutContents = () => {
    return (
      <div className="unauthorizedMode">
        <SignIn
          setSignedIn={setSignedIn}
          setSignedInUserName={setSignedInUserName}
        />
      </div>
    )
  }

  const contents = () => {
    if (signedIn === null) {
      return (
        <div>Checking signed in status...</div>
      )
    } else if (signedIn === true) {
      return signedInContents()
    } else if (signedIn === false) {
      return signedOutContents()
    }
  }


  return (
    <div className="App">
      <MuiThemeProvider theme={appTheme}>
        <Header
          signedIn={signedIn}
          setSignedIn={setSignedIn}
          signedInUserName={signedInUserName}
          setSignedInUserName={setSignedInUserName}
        />
        { contents() }
      </MuiThemeProvider>
    </div>
  );
}

export default App;
