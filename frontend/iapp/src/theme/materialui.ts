import {createMuiTheme} from '@material-ui/core/styles'


export const appTheme = createMuiTheme({
  palette: {
    primary: {
      light: '#757ce8',
      main: '#d32f2f',
      dark: '#002884',
      contrastText: '#fff',
    },
    secondary: {
      light: '#ff7961',
      main: '#651fff',
      dark: '#ba000d',
      contrastText: '#000',
    },
  },
});
