import React from 'react';
import Container from '@material-ui/core/Container';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import TwitterUserSearchButton, { SearchButtonProps } from '../components/TwitterUserSearchButton';
import TwitterUserSearchTextBox, { SearchTextBoxProps } from '../components/TwitterUserSearchTextBox';


export type SearchWidgetProps = SearchButtonProps & SearchTextBoxProps;

const TwitterUserSearchWidget: React.FC<SearchWidgetProps> = (props: SearchWidgetProps) => {
  return (
    // <Container component="main" maxWidth="md">
      <Paper elevation={3} style={{padding: "10px 50px 10px", marginTop: 20}}>
        <Grid container  alignItems="center" justify="center">
          <Grid item xs={8}>
            <TwitterUserSearchTextBox onSearchTextChange={props.onSearchTextChange} />
          </Grid>
          <Grid item xs={4}>
            <TwitterUserSearchButton onSearchButtonClick={props.onSearchButtonClick} />
          </Grid>
        </Grid>
        <div  style={{backgroundColor: '#FF5F00'}}></div>
        <TwitterUserSearchTextBox onSearchTextChange={props.onSearchTextChange} />
        <TwitterUserSearchButton onSearchButtonClick={props.onSearchButtonClick} />
      </Paper>
    // </Container>
  )
}

export default TwitterUserSearchWidget;