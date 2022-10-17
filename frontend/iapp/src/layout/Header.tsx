import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import MenuIcon from '@material-ui/icons/Menu';
import { useRecoilState, useRecoilValue } from 'recoil';
import { AuthState, rclSignOut, rclStateAuth } from '../states/Recoil';


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
    userName: {
      color: "#000000",
    },
  }),
);

type Props = {}

const Header: React.FC<Props> = (props: Props) => {
  const classes = useStyles();
  const authState = useRecoilValue<AuthState>(rclStateAuth);
  const [signedOut, setSignOut] = useRecoilState(rclSignOut);

  const signOut = () => {
    if (authState.isSignedIn) {
      setSignOut(true)
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
          <Typography className={classes.userName}>
            {authState.signedInUsername}
          </Typography>
          <Button
            color="inherit"
            onClick={() => { if (authState.isSignedIn) { signOut() } }}>
            {authState.isSignedIn ? 'SIGN OUT' : 'SIGN IN'}
          </Button>
        </Toolbar>
      </AppBar>
    </div>
  )
}

export default Header;
