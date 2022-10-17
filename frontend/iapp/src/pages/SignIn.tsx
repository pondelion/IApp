import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import {
  AuthenticationDetails, CognitoUser
} from 'amazon-cognito-identity-js';
import axios from 'axios';
import React from 'react';
//@ts-ignore
import { Service } from 'axios-middleware';
import { useRecoilState } from 'recoil';
import '../App.css';
import { userPool } from '../aws/Cognito';
import Header from '../layout/Header';
import {
  rclSignOut,
  rclStateAuth,
  rclStateGuestMode
} from '../states/Recoil';


type Props = {}

const SignIn: React.FC<Props> = (props: Props) => {
  const [username, setUserName] = React.useState<string>('')
  const [password, setPassword] = React.useState<string>('')
  const [errMsg, setErrMsg] = React.useState<string>('')
  const [authState, setAuthState] = useRecoilState(rclStateAuth);
  const [signOut, setSignOut] = useRecoilState(rclSignOut);
  const [guestMode, setGuestMode] = useRecoilState(rclStateGuestMode);
  const changedUserNameHaldler = (e: any) => setUserName(e.target.value)
  const changedPasswordHandler = (e: any) => setPassword(e.target.value)
  const axiosService = new Service(axios);

  const signIn = () => {
    const authenticationDetails = new AuthenticationDetails({
      Username: username,
      Password: password
    })
    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool
    })

    cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: (result: any) => {
        // login success
        console.log('result: ' + result)
        const accessToken = result.getAccessToken().getJwtToken();
        const idToken = result.idToken.jwtToken;
        console.log('idToken: ' + idToken)
        setErrMsg('');
        setAuthState({
          isSignedIn: true,
          signedInUsername: username,
          accessToken: idToken,
        });
        axiosService.register({
          onRequest(config: any) {
            config.headers['Authorization'] = `Bearer ${idToken}`;
            return config;
          }
        });
      },
      onFailure: (err: any) => {
        console.error(err);
        setErrMsg(err.message);
      }
    })
  }

  return (
    <div>
      <Header />
      <Container component="main" maxWidth="xs">
        <Paper elevation={3} style={{ padding: "10px 50px 30px", marginTop: 20 }}>
          <div className="SignIn">
            <h1>
              Sign In
            </h1>
            <div>
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="User Name"
                name="username"
                autoComplete="User Name"
                onChange={changedUserNameHaldler}
              />
            </div>
            <div>
              <TextField
                type="password"
                margin="normal"
                required
                fullWidth
                id="password"
                label="Password"
                name="password"
                autoComplete="Password"
                onChange={changedPasswordHandler}
              />
            </div>
            <div style={{ marginTop: 20 }}>
              <Button variant="contained" color="primary" onClick={signIn}>Sign In</Button>
            </div>
            <div style={{ color: 'red', fontWeight: 'bold', marginTop: 20 }}>{errMsg}</div>
          </div>
        </Paper>
      </Container>
    </div>
  )
}

export default SignIn