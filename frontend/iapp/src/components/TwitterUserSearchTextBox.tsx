import React from 'react';
import TextField from '@material-ui/core/TextField'


export type SearchTextBoxProps = {
  onSearchTextChange: React.ChangeEventHandler;
}

const TwitterUserSearchTextBox: React.FC<SearchTextBoxProps> = (props: SearchTextBoxProps) => {
  return (
    <TextField
      // margin="normal"
      required
      fullWidth
      id="username"
      label="User Name"
      name="username"
      autoComplete="User Name"
      onChange={props.onSearchTextChange}
    />
  )
}

export default TwitterUserSearchTextBox;