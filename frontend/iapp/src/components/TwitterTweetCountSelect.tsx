import { TextField } from '@material-ui/core';
import React, { useState } from 'react';


export type TweetCountSelectProps = {
  onValueChanged?: (tweetCount: number) => void
}

const TwitterTweetCountSelect: React.FC<TweetCountSelectProps> = (props: TweetCountSelectProps) => {
  const [tweetCount, setTweetCount] = useState<number>(50);
  const min: number = 1;
  const max: number = 500;

  return (
    <TextField
      name="TwitterTweetCount"
      label="Max Tweet Count To Fetch"
      type="number"
      InputProps={{ inputProps: { min: min, max: max } }}
      fullWidth
      variant="outlined"
      value={tweetCount}
      onChange={(e) => {
        var value = parseInt(e.target.value, 10);
        if (value > max) value = max;
        if (value < min) value = min;
        setTweetCount(value);
        if (props.onValueChanged) {
          props.onValueChanged(value);
        }
      }}
    >
    </TextField>
  )
}

export default TwitterTweetCountSelect;
