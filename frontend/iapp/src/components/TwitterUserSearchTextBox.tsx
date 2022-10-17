import TextField from '@material-ui/core/TextField';
import React from 'react';


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
      label="User Name | Screen Name"
      name="username"
      autoComplete="User Name | Screen Name"
      onChange={(e) => props.onSearchTextChange(e)}
    />
  )
}

export default TwitterUserSearchTextBox;