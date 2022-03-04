import multiprocessing
from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from typing import Dict, List

from ..base_crawler import BaseCrawler
from .api import API


class KeywordCrawler(BaseCrawler):

    def __init__(
        self,
        keywords: List[str] = [],
        count: int = 200,
    ):
        """[summary]

        Args:
            keywords (List[str], optional): [description]. Defaults to [].
            count (int, optional): [description]. Defaults to 200.
        """
        self._keywords = keywords
        self._CPU_COUNT = multiprocessing.cpu_count()
        self._count = count

    def set_keywords(
        self,
        keywords: List[str]
    ) -> None:
        """[summary]
        
        Args:
            keywords (List[str]): [description]
        """
        self._keywords = keywords

    def add_keywords(
        self,
        keywords: List[str]
    ) -> None:
        """[summary]

        Args:
            keywords (List[str]): [description]
        """
        self._keywords += keywords

    def run(
        self,
        keywords: List[str] = [],
        count: int = None,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        parallel: bool = True,
    ) -> None:
        """[summary]

        Args:
            keywords (List[str], optional): [description]. Defaults to [].
            count (int, optional): [description]. Defaults to None.
            callback (Callback, optional): [description]. Defaults to None.
        """
        self.add_keywords(keywords)
        if count is not None:
            self._count = count

        if parallel:
            sub_keywords = [
                self._keywords[i::self._CPU_COUNT] for i in range(self._CPU_COUNT)
            ]
            processes = [
                Process(
                    target=self._crawl,
                    args=(keywords, self._count, callback)
                ) for keywords in sub_keywords
            ]
            [p.start() for p, keywords in zip(processes, sub_keywords) if len(keywords) != 0]
            [p.join() for p, keywords in zip(processes, sub_keywords) if len(keywords) != 0]
        else:
            self._crawl(
                keywords=self._keywords,
                count=self._count,
                callback=callback
            )

    def _crawl(
        self,
        keywords: List[str],
        count: int,
        callback: BaseCrawler.Callback,
    ) -> None:
        """[summary]

        Args:
            keywords (List[str]): [description]
        """
        for keyword in keywords:
            args = {
                'keyword': keyword,
            }
            try:
                results = API.search(
                    q=keyword,
                    count=count
                )
                callback.on_finished(results, args)
            except Exception as e:
                callback.on_failed(e, args)
