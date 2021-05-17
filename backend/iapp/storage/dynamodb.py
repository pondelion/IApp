from typing import Dict, List

from boto3.dynamodb.conditions import Key

from ..aws.resource_provider import DYNAMO_DB
from ..utils.logger import Logger
from .storage import Storage


class DynamoDB(Storage):

    def __init__(self, table_name: str):
        self._table_name = table_name
        try:
            self._table = DYNAMO_DB.Table(self._table_name)
        except Exception as e:
            Logger.e('DynamoDB', f'Failed at DYNAMO_DB.Table({self._table}) : {e}')
            raise e

    def save(
        self,
        items: List[Dict],
        use_batch_writer: bool = False,
    ) -> List:
        if not isinstance(items, list):
            items = [items]

        responses = []

        if use_batch_writer:
            with self._table.batch_writer() as batch:
                for item in items:
                    try:
                        responses.append(
                            batch.put_item(
                                Item=item,
                            )
                        )
                    except Exception as e:
                        Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB. Skipping : {e}')
        else:
            for item in items:
                try:
                    responses.append(
                        self._table.put_item(
                            TableName=self._table_name,
                            Item=item,
                        )
                    )
                except Exception as e:
                    Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB. Skipping : {e}')

        return responses

    def get(
        self,
        key_condition_expression = None,
        filter_expression = None,
        **kwargs,
    ) -> List[Dict]:
        items = []
        try:
            response = self._table.query(
                KeyConditionExpression=key_condition_expression,
                FilterExpression=filter_expression,
            )
            items += response['Items']

            while 'LastEvaluatedKey' in response:
                response = self._table.query(
                    KeyConditionExpression=key_condition_expression,
                    FilterExpression=filter_expression,
                    ExclusiveStartKey=response['LastEvaluatedKey'],
                    **kwargs
                )
                items += response['Items']
        except Exception as e:
            Logger.e('DynamoDB#partitionkey_query', f'Failed to query : {e}')
            return []

        return items

    def partitionkey_query(
        self,
        partition_key_name: str,
        partition_key: str,
    ) -> List[Dict]:
        return self.get(
            key_condition_expression=Key(partition_key_name).eq(partition_key),
        )

    def get_list(self) -> List[Dict]:
         # scan
         raise NotImplementedError
