import React from 'react';
import { DataGrid, GridRowParams } from '@material-ui/data-grid';


const dataGridParams = {
  'columns': [
    { field: 'id', headerName: 'id', width: 5 },
    { field: 'datetime', headerName: 'datetime', width: 200 },
    { field: 'tweet', headerName: 'tweet', width: 500 },
  ],
  'pageSize': 10,
}

export type TweetListProps = {
  tweets: any,
  onRowClick: (param: GridRowParams, event: React.MouseEvent<Element, MouseEvent>) => void,
}

export type TweetDataType = {
  id: number;
  datetime: string;
  tweet: string;
}[]

const RawTweetList: React.FC<TweetListProps> = (props: TweetListProps) => {
  return (
    <div>
      <DataGrid
        autoHeight
        rows={ props.tweets }
        columns={ dataGridParams.columns }
        pageSize={ dataGridParams.pageSize }
        onRowClick={ props.onRowClick }
      />
    </div>
  )

}

export default RawTweetList;