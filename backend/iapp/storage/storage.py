from abc import ABCMeta, abstractmethod
from enum import Enum


class Storage(metaclass=ABCMeta):

    @abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_list(self, **kwargs):
        raise NotImplementedError


class StorageType(Enum):
    S3 = 's3'
    DYNAMO_DB = 'dynamo_db'
