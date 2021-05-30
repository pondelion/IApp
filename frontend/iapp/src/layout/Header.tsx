import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import { userPool } from '../aws/Cognito';


const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
  }),
);

type Props = {
  signedIn: boolean | null,
  setSignedIn: React.Dispatch<React.SetStateAction<boolean|null>>
}

const Header: React.FC<Props> = (props: Props) => {
  const classes = useStyles();

  const signOut = () => {
    const cognitoUser = userPool.getCurrentUser()
    if (cognitoUser) {
      cognitoUser.signOut()
      localStorage.clear()
      console.log('signed out')
      props.setSignedIn(false)
    } else {
      localStorage.clear()
      console.log('no user signing in')
    }
  }

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <IconButton edge="start" className={classes.menuButton} color="inherit" arial-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
            IApp
          </Typography>
          <Button
            color="inherit"
            onClick={() => {if (props.signedIn) {signOut()}}}>
              {props.signedIn ? 'SIGN OUT' : 'SIGN IN'}
          </Button>
        </Toolbar>
      </AppBar>
    </div>
  )
}

export default Header;
