import { Button, Tooltip } from '@material-ui/core';
import { DataGrid, GridRowParams, MuiEvent } from '@material-ui/data-grid';
import React, { SyntheticEvent } from 'react';


const dataGridParams = {
  'columns': [
    {
      field: 'id',
      headerName: 'id',
      width: 5
    },
    {
      field: 'datetime',
      headerName: 'datetime',
      width: 200
    },
    {
      field: 'tweet',
      headerName: 'tweet',
      width: 450,
      renderCell: (params: any) => (
        <Tooltip title={params.value}>
          <span>{params.value}</span>
        </Tooltip>
      ),
    },
    {
      field: 'button',
      headerName: 'button',
      width: 100,
      renderCell: (params: any) => (
        <Button variant="contained" color="secondary">詳細</Button>
      ),
    }
  ],
  'pageSize': 10,
}

export type TweetListProps = {
  tweets: any,
  onRowClick: (param: GridRowParams, event: MuiEvent<SyntheticEvent<Element, Event>>) => void,
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
        rows={props.tweets}
        columns={dataGridParams.columns}
        pageSize={dataGridParams.pageSize}
        onRowClick={props.onRowClick}
      />
    </div>
  )

}

export default RawTweetList;