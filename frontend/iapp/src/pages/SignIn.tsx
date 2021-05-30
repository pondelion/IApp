import React from 'react'
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField'
import Container from '@material-ui/core/Container'
import Paper from '@material-ui/core/Paper';
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails
} from 'amazon-cognito-identity-js'
import '../App.css';
import { userPool } from '../aws/Cognito';


type Props = {
  setSignedIn: React.Dispatch<React.SetStateAction<boolean|null>>;
}

const SignIn: React.FC<Props> = (props: Props) => {
  const [username, setUserName] = React.useState<string>('')
  const [password, setPassword] = React.useState<string>('')
  const [errMsg, setErrMsg] = React.useState<string>('')
  const changedUserNameHaldler = (e: any) => setUserName(e.target.value)
  const changedPasswordHandler = (e: any) => setPassword(e.target.value)

  const signIn = () => {
    const authenticationDetails = new AuthenticationDetails({
      Username : username,
      Password : password
    })
    const cognitoUser = new CognitoUser({
      Username: username,
      Pool: userPool
    })

    cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: (result) => {
        console.log('result: ' + result)
        const accessToken = result.getAccessToken().getJwtToken()
        console.log('AccessToken: ' + accessToken)
        setUserName('')
        setPassword('')
        setErrMsg('')
        props.setSignedIn(true)
      },
      onFailure: (err) => {
        console.error(err)
        setErrMsg(err.message)
      }
    })
  }

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} style={{padding: "10px 50px 30px", marginTop: 20}}>
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
        <div style={{marginTop: 20}}>
          <Button variant="contained" color="primary" onClick={signIn}>Sign In</Button>
        </div>
        <div style={{color:'red', fontWeight:'bold', marginTop: 20}}>{errMsg}</div>
      </div>
      </Paper>
    </Container>
  )
}

export default SignIn