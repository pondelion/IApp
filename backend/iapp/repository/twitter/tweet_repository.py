from typing import List, Union


class TweetRepository(Repository):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = None,
        media_storage: Storage,
    ):
        super().__init__(storage_or_db)
        self._media_storage = media_storage

    def save(self, data: Union[Tweet, List[Tweet]]) -> None:
        