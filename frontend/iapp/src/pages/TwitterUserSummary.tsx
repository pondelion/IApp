import React from 'react';
import TwitterUserSearchWidget, { SearchWidgetProps } from '../containers/TwitterUserSearchWidget';
import TwitterUserSummaryTab, { TwitterUserSummaryTabProps } from '../containers/TwitterUserSummaryTab';
import { TweetDataType } from '../containers/RawTweetList';
import Container from '@material-ui/core/Container';


export type Props = {};

const TwitterUserSummary: React.FC<Props> = (props: Props) => {
  const dummyTweetData = [
    { id: 1, datetime: '2021-05-31 10:00', tweet: 'tweet1' },
    { id: 2, datetime: '2021-05-31 11:00', tweet: 'tweet2' },
    { id: 3, datetime: '2021-05-31 12:00', tweet: 'tweet3' },
  ]
  const [tweets, setTweets] = React.useState<TweetDataType>([]);

  return (
    <Container component="main" maxWidth="lg">
      <Container component="main" maxWidth="md">
        <TwitterUserSearchWidget
          onSearchButtonClick={() => { setTweets(dummyTweetData) }}
          onSearchTextChange={() => {}}
        />
      </Container>
      <Container component="main" maxWidth="md" style={{marginTop: 20}}>
        <TwitterUserSummaryTab tweets={tweets} />
      </Container>
    </Container>
  )
}

export default TwitterUserSummary;
