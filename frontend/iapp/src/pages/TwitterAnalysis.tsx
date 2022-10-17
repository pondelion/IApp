import Container from '@material-ui/core/Container';
import React from 'react';
import TwitterAPI from '../api_client/TwitterAPI';
import { ImgData } from '../components/ImageGallery';
import { TweetDataType } from '../containers/RawTweetList';
import TwitterUserSearchWidget from '../containers/TwitterUserSearchWidget';
import TwitterUserSummaryTab from '../containers/TwitterUserSummaryTab';
import Header from '../layout/Header';


export type Props = {};

const TwitterAnalysis: React.FC<Props> = (props: Props) => {
  const dummyTweetData = [
    { id: 1, datetime: '2021-05-31 10:00', tweet: 'tweet1' },
    { id: 2, datetime: '2021-05-31 11:00', tweet: 'tweet2' },
    { id: 3, datetime: '2021-05-31 12:00', tweet: 'tweet3' },
  ]
  const dummyImages = [
    {
      original: 'https://cdn.pixabay.com/photo/2020/03/09/23/04/plum-4917370_960_720.jpg',
      thumbnail: 'https://cdn.pixabay.com/photo/2020/03/09/23/04/plum-4917370_960_720.jpg',
    },
    {
      original: 'https://cdn.pixabay.com/photo/2020/02/21/18/43/kosmeen-4868375_960_720.jpg',
      thumbnail: 'https://cdn.pixabay.com/photo/2020/02/21/18/43/kosmeen-4868375_960_720.jpg',
    },
    {
      original: 'https://cdn.pixabay.com/photo/2016/04/16/12/50/chrysanthemum-1332994_960_720.jpg',
      thumbnail: 'https://cdn.pixabay.com/photo/2016/04/16/12/50/chrysanthemum-1332994_960_720.jpg',
    },
  ];
  const [tweets, setTweets] = React.useState<TweetDataType>([]);
  const [searchName, setSearchName] = React.useState<string>('');
  const [glrImages, setGlrImages] = React.useState<ImgData[]>(dummyImages);
  const twitterAPI = new TwitterAPI();

  const onSearchButtonClick = () => {
    setTweets(dummyTweetData);
    console.log(searchName);
    twitterAPI
      .getTweetByUsername(searchName, 50)
      .then((res) => {
        console.log(res.data);
        setTweets(res.data.map((v: any) => {
          return {
            id: v.id,
            datetime: v.tweet_created_at,
            tweet: v.text
          }
        }));
        twitterAPI
          .getMediaByUsername(searchName)
          .then((res) => {
            console.log(res.data);
            setGlrImages(res.data.map((v: any) => {
              return {
                original: v.media_url,
                thumbnail: v.media_url,
              }
            }));
          })
          .catch((err) => {
            console.log(err);
          })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return (
    <div>
      <Header />
      <Container component="main" maxWidth="lg">
        <Container component="main" maxWidth="md">
          <TwitterUserSearchWidget
            onSearchButtonClick={() => { onSearchButtonClick() }}
            onSearchTextChange={(event) => { setSearchName((event as any).target.value) }}
          />
        </Container>
        <Container component="main" maxWidth="md" style={{ marginTop: 20 }}>
          <TwitterUserSummaryTab tweets={tweets} images={glrImages} />
        </Container>
      </Container>
    </div>
  )
}

export default TwitterAnalysis;
