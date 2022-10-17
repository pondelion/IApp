import { MuiThemeProvider } from '@material-ui/core/styles';
import axios from 'axios';
//@ts-ignore
import { Service } from 'axios-middleware';
import { useEffect } from 'react';
import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import { useRecoilState } from 'recoil';
import './App.css';
import { userPool } from './aws/Cognito';
import SignIn from './pages/SignIn';
import TwitterAnalysis from './pages/TwitterAnalysis';
import {
  rclSignOut,
  rclStateAuth,
  rclStateGuestMode
} from './states/Recoil';
import { appTheme } from './theme/materialui';


function App() {
  const [authState, setAuthState] = useRecoilState(rclStateAuth);
  const [signOut, setSignOut] = useRecoilState(rclSignOut);
  const [guestMode, setGuestMode] = useRecoilState(rclStateGuestMode);
  const axiosService = new Service(axios);
  console.log(authState.isSignedIn);
  console.log(authState.signedInUsername);

  useEffect(() => {
    if (!guestMode) {
      const cognitoUser = userPool.getCurrentUser();
      if (cognitoUser) {  // Already signed in.
        cognitoUser.getSession((err: any, session: any) => {
          if (session.isValid()) {
            setAuthState({
              isSignedIn: true,
              signedInUsername: cognitoUser.getUsername(),
              // accessToken: session.accessToken.jwtToken,
              accessToken: session.idToken.jwtToken,
            });
            axiosService.register({
              onRequest(config: any) {
                config.headers['Authorization'] = `Bearer ${session.idToken.jwtToken}`;
                return config;
              }
            });
          } else {
            setSignOut(true);
            console.log('invalid session');
          }
        });
        console.log('signed in');
      } else {
        setSignOut(true);
        console.log('not signed in');
      }
    }
  }, [authState, guestMode]);

  return (
    <div className="App">
      <MuiThemeProvider theme={appTheme}>
        <Router basename={process.env.PUBLIC_URL}>
          <Routes >
            <Route path="/" element={authState.isSignedIn ? <TwitterAnalysis /> : <Navigate to="/signin" replace />} />
          </Routes >
          <Routes >
            <Route path="/signin" element={authState.isSignedIn ? <Navigate to="/" replace /> : <SignIn />} />
          </Routes >
        </Router>
      </MuiThemeProvider>
    </div>
  );
}

export default App;
