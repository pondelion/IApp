from abc import ABCMeta, abstractmethod

from ..storage import Storage


class Repository(metaclass=ABCMeta):

    def __init__(
        self,
        storage: Storage,
    ):
        self._storage = storage

    @abstractmethod
    def save(self, data) -> None:
        raise NotImplementedError
