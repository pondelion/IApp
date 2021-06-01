from abc import ABCMeta, abstractmethod
from typing import List, Union

from ..storage import Storage, StorageType
from ..db import DB, DBType


class Repository(metaclass=ABCMeta):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = None
    ):
        if storage is None and db is None:
            raise ValueError('At least storage or db must be specified.')
        if db is not None:
            self._validate_db(db)
        if storage is not None:
            self._validate_storage(storage)
        self._storage = storage
        self._db = db

    def save(self, data, filepath: str) -> None:
        if self._storage is not None:
            self._save_storage(data, filepath)
        if self._db is not None:
            self._save_db(data)

    @abstractmethod
    def _save_storage(self, data, filepath: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def _save_db(self, data) -> None:
        raise NotImplementedError

    @abstractmethod
    def _supported_storage_types(self) -> List[StorageType]:
        raise NotImplementedError

    @abstractmethod
    def _supported_db_types(self) -> List[DBType]:
        raise NotImplementedError

    def _validate_db(self, db: DB):
        supported_db_types = self._supported_db_types()
        if not any([db.type==s_db_type for s_db_type in supported_db_types]):
            raise ValueError(f'{db} is not supported db.')

    def _validate_storage(self, storage: Storage):
        supported_storage_types = self._supported_storage_types()
        if not any([storage.type==s_storage_type for s_storage_type in supported_storage_types]):
            raise ValueError(f'{storage} is not supported storage.')
