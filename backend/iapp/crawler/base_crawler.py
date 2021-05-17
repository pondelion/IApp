from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union
from threading import Thread

from overrides import overrides

from .callback import (
    Callback,
    DefaultCallback,
    ProgressResponse
)
from ..utils.logger import Logger


class BaseCrawler(metaclass=ABCMeta):

    def crawl(
        self,
        async_mode: bool = False,
        callback: Callback = DefaultCallback(),
        **kwargs,
    ) -> Any:
        self._async_mode = async_mode
        self._callback = callback
        if async_mode:
            self._thread = Thread(
                target=self._crawl,
                kwargs=kwargs,
            )
            self._thread.start()
            return self._thread
        else:
            return self._crawl(callback=None)

    @abstractmethod
    def _crawl(
        self,
        **kwargs,
    ) -> Any:
        raise NotImplementedError

    def _on_completed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        # if self._async_mode:
        #     self._callback.on_completed(data, kwargs)
        # else:
        #     return (data, kwargs)
        self._callback.on_completed(data, kwargs)
        return (data, kwargs)

    def _on_progressed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> ProgressResponse:
        return self._callback.on_progressed(data, kwargs)

    def _on_failed(
        self,
        e: Exception,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        if self._async_mode:
            self._callback.on_failed(e, kwargs)
        else:
            raise e
