from datetime import datetime
from typing import List, Dict

import requests

from ..base_crawler import BaseCrawler
from ...utils.logger import Logger


class CompanyAnnouncementCrawler(BaseCrawler):

    def __init__(
        self
    ):
        self._TDNET_URL_FMT = 'https://webapi.yanoshin.jp/webapi/tdnet/list/{start_dt}-{end_dt}.json'

    def run(
        self,
        start_dt: datetime,
        end_dt: datetime,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        """[summary]
        
        Args:
            start_dt (datetime): [description]
            end_dt (datetime): [description]
            callback (BaseCrawler.Callback, optional): [description]. Defaults to BaseCrawler.DefaultCallback().
        """
        kwargs = {
            'start_dt': start_dt,
            'end_dt': end_dt,
        }
        res = requests.get(
            self._TDNET_URL_FMT.format(
                start_dt=start_dt.strftime('%Y%m%d'),
                end_dt=end_dt.strftime('%Y%m%d')
            )
        ).json()
        if not self._validate_response(res):
            Logger.e(
                'CompanyAnnouncementCrawler#run',
                f'Failed to fetch data from TDnet'
            )
            callback.on_failed(
                Exception('Failed to fetch data from TDnet'),
                kwargs
            )
        res = self._parse_data(res)
        if len(res) == 300:
            Logger.w(
                'CompanyAnnouncementCrawler#run',
                'Data length is 300. Some data might be omitted.'
            )

        callback.on_finished(
            res,
            kwargs,
        )

    def _validate_response(
        self,
        res,
    ) -> bool:
        """[summary]
        
        Args:
            res ([type]): [description]
        
        Returns:
            bool: [description]
        """
        return 'items' in res

    def _parse_data(
        self,
        json_data: Dict,
    ) -> List:
        """[summary]
        
        Args:
            json_data (Dict): [description]
        
        Returns:
            List: [description]
        """
        return [d['Tdnet'] for d in json_data['items']]
