from typing import List, Union

from overrides import overrides


class TweetRepository(Repository):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = None,
        media_storage: Storage = None,
    ):
        super().__init__(storage, db)
        self._validaet_db(db)
        self._media_storage = media_storage

    @overrides
    def _save_storage(
        self, data: Union[Tweet, List[Tweet]],
        filepath: str
    ) -> None:
        raise NotImplementedError("""
            Storage saving is not supported for tweet data.
        """)

    @overrides
    def _save_db(self, data: Union[Tweet, List[Tweet]]) -> None:
        if self

    def _validaet_db(self, db: DB):
        if db is not None and db.type != DBType.DYNAMO_DB:
            raise ValueError('Only DynamoDB is sopported for db for now.')
