from abc import ABCMeta, abstractmethod
from typing import Dict, Any

import pandas as pd


class BaseCrawler(metaclass=ABCMeta):

    class Callback(metaclass=ABCMeta):

        @abstractmethod
        def on_finished(
            self,
            data: pd.DataFrame,
            args: Dict,
        ) -> None:
            """[summary]

            Args:
                data (pd.DataFrame): [description]
                args (Dict): [description]

            Raises:
                NotImplementedError: [description]
            """
            raise NotImplementedError

        @abstractmethod
        def on_failed(
            self,
            e: Exception,
            args: Dict,
        ) -> None:
            """[summary]

            Args:
                e (Exception): [description]
                args (Dict): [description]

            Raises:
                NotImplementedError: [description]
            """
            raise NotImplementedError

    class DefaultCallback(Callback):

        def on_finished(
            self,
            data: pd.DataFrame,
            args: Dict,
        ) -> None:
            pass

        def on_failed(
            self,
            e: Exception,
            args: Dict,
        ) -> None:
            pass

    def __init__(self):
        """init"""
        pass

    @abstractmethod
    def run(self) -> Any:
        """run crawl
        Subclass must implemets this method
        """
        raise NotImplementedError
