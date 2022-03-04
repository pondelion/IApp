from abc import ABCMeta, abstractmethod
from enum import Enum


class StorageType(Enum):
    S3 = 's3'


class Storage(metaclass=ABCMeta):

    @abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_filelist(self, **kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> StorageType:
        raise NotImplementedError
