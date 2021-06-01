from typing import List, Union

from overrides import overrides

from ..repository import Repository
from ...storage import Storage, StorageType
from ...db import DB, DBType


class UserRepository(Repository):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = None,
    ):
        super().__init__(storage, db)

    def _save_storage(
        self, data: Union[TwitterUser, List[TwitterUser]],
        filepath: str
    ) -> None:
        raise NotImplementedError("""
            Storage saving is not supported for tweet data.
        """)

    def _save_db(self, data: Union[TwitterUser, List[TwitterUser]]) -> None:
        if not isinstance(data, list):
            data = [data]
        json_data = [d.json() for d in data]
        self.db.save(json_data)

    @overrides
    def _supported_storage_types(self) -> List[StorageType]:
        return []

    @overrides
    def _supported_db_types(self) -> List[DBType]:
        return [DBType.DYNAMO_DB]
