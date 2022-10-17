import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import React from 'react';
import TwitterTweetCountSelect from '../components/TwitterTweetCountSelect';
import TwitterUserSearchButton, { SearchButtonProps } from '../components/TwitterUserSearchButton';
import TwitterUserSearchTextBox, { SearchTextBoxProps } from '../components/TwitterUserSearchTextBox';


export type SearchWidgetProps = SearchButtonProps & SearchTextBoxProps;

const TwitterUserSearchWidget: React.FC<SearchWidgetProps> = (props: SearchWidgetProps) => {
  return (
    // <Container component="main" maxWidth="md">
    <Paper elevation={3} style={{ padding: "10px 30px 10px", marginTop: 20 }}>
      <Grid container alignItems="center" justify="center">
        <Grid item xs={6}>
          <TwitterUserSearchTextBox onSearchTextChange={props.onSearchTextChange} />
        </Grid>
        <Grid item xs={3} style={{ padding: "0px 10px 0px 10px" }}>
          <TwitterTweetCountSelect />
        </Grid>
        <Grid item xs={3} style={{ background: "#FFFFFF" }}>
          <TwitterUserSearchButton onSearchButtonClick={props.onSearchButtonClick} />
        </Grid>
      </Grid>
      {/* <div  style={{backgroundColor: '#FF5F00'}}></div>
        <TwitterUserSearchTextBox onSearchTextChange={props.onSearchTextChange} />
        <TwitterUserSearchButton onSearchButtonClick={props.onSearchButtonClick} /> */}
    </Paper>
    // </Container>
  )
}

export default TwitterUserSearchWidget;