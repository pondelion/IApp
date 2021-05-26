from abc import ABCMeta, abstractmethod
from typing import List, Union

from ..storage import Storage
from ..db import DB


class Repository(metaclass=ABCMeta):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = None
    ):
        if storage is None and db is None:
            raise ValueError('At least storage or db must be specified.')
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
