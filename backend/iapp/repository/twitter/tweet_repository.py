from typing import List, Union


class TweetRepository(Repository):

    def __init__(
        self,
        storage: Storage,
        media_storage: Storage,
    ):
        super().__init__(storage)
        self._media_storage = media_storage

    def save(self, data: Union[Tweet, List[Tweet]]) -> None:
        