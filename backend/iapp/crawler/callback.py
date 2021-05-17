from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union
from enum import Enum

from overrides import overrides


class ProgressResponse(Enum):
    KEEP_CRAWLING = 'keep_crawling'
    STOP_CRAWLING = 'stop_crawling'


class Callback(metaclass=ABCMeta):

    @abstractmethod
    def on_completed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_progressed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> ProgressResponse:
        raise NotImplementedError

    @abstractmethod
    def on_failed(
        self,
        e: Exception,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        raise NotImplementedError


class DefaultCallback(Callback):

    @overrides
    def on_completed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        pass

    @overrides
    def on_progressed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> ProgressResponse:
        return ProgressResponse.KEEP_CRAWLING

    @overrides
    def on_failed(
        self,
        e: Exception,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        pass
