import React from 'react';
import Button from '@material-ui/core/Button';
import SearchIcon from '@material-ui/icons/Search';


const styles = {
  webButton: {
    textTransform: 'none',
  }
}

export type SearchButtonProps = {
  onSearchButtonClick: React.MouseEventHandler;
}

const TwitterUserSearchButton: React.FC<SearchButtonProps> = (props: SearchButtonProps) => {
  return (
    <Button
      variant="contained"
      color="secondary"
      onClick={props.onSearchButtonClick}
      startIcon={<SearchIcon />}
      style={{textTransform: 'none', color: 'white'}}
    >
      Search Tweet
    </Button>
  )

}

export default TwitterUserSearchButton;