import React from 'react';
import TwitterUserSearchWidget, { SearchWidgetProps } from '../containers/TwitterUserSearchWidget';
import TwitterUserSummaryTab from '../containers/TwitterUserSummaryTab';
import Container from '@material-ui/core/Container';


export type Props = SearchWidgetProps

const TwitterUserSummary: React.FC<Props> = (props: Props) => {
  return (
    <Container component="main" maxWidth="lg">
      <Container component="main" maxWidth="md">
        <TwitterUserSearchWidget
          onSearchButtonClick={props.onSearchButtonClick}
          onSearchTextChange={props.onSearchTextChange}
        />
      </Container>
      <Container component="main" maxWidth="md" style={{marginTop: 20}}>
        <TwitterUserSummaryTab />
      </Container>
    </Container>
  )
}

export default TwitterUserSummary;
