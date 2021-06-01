import React from 'react';
import { makeStyles, Theme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import RawTweetList from './RawTweetList';


interface TabPanelProps {
  children?: React.ReactNode;
  index: any;
  value: any;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: any) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

export type TwitterUserSummaryTabProps = {
  tweets: any
}

const TwitterUserSummaryTab: React.FC<TwitterUserSummaryTabProps> = (props: TwitterUserSummaryTabProps) => {

  // const tweetData = [
  //   { id: 1, datetime: '2021-05-31 10:00', tweet: 'tweet1' },
  //   { id: 2, datetime: '2021-05-31 11:00', tweet: 'tweet2' },
  //   { id: 3, datetime: '2021-05-31 12:00', tweet: 'tweet3' },
  // ]

  const [selectedTab, setSelectedTab] = React.useState(0);
  // const [tweets, setTweets] = React.useState(tweetData);

  const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setSelectedTab(newValue);
  };

  return (
    <div>
      <AppBar position="static">
        <Tabs value={selectedTab} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Raw Tweet" {...a11yProps(0)} style={{textTransform: 'none'}}/>
          <Tab label="Tweet Statistics" {...a11yProps(1)} style={{textTransform: 'none'}}/>
        </Tabs>
      </AppBar>
      <TabPanel value={selectedTab} index={0}>
        <RawTweetList
          tweets={props.tweets}
          onRowClick={(params, event) => console.log(params)}
        />
      </TabPanel>
      <TabPanel value={selectedTab} index={1}>
        <div />i
      </TabPanel>
    </div>
  );
}

export default TwitterUserSummaryTab;