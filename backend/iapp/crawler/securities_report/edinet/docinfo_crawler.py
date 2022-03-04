from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Dict
import time

import requests
import pandas as pd

from ...base_crawler import BaseCrawler


class EdinetDocInfoCrawler(BaseCrawler):

    def run(
        self,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        start: datetime=datetime.now()-relativedelta(years=5),
        end: datetime=datetime.now()
    ) -> None:

        DOCINFO_URL_FMT = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={date}&type=2'

        for dt in pd.date_range(start, end, freq='D')[::-1]:
            date_str = dt.strftime('%Y-%m-%d')
            params = {'date': date_str}
            docinfo_url = DOCINFO_URL_FMT.format(date=date_str)
            try:
                res = requests.get(docinfo_url)
                docinfo_jsons = res.json()['results']
                df_docinfo = self._docjsons2df(docinfo_jsons)
                callback.on_finished(df_docinfo, params)
            except Exception as e:
                callback.on_failed(e, params)
            time.sleep(0.5)

    def _docjsons2df(self, docjsons: List[Dict]) -> pd.DataFrame:
        doc_descriptions = [r['docDescription'] for r in docjsons]
        doc_ids = [r['docID'] for r in docjsons]
        filer_names = [r['filerName'] for r in docjsons]
        period_starts = [r['periodStart'] for r in docjsons]
        period_ends = [r['periodEnd'] for r in docjsons]
        submit_datetimes = [r['submitDateTime'] for r in docjsons]
        PDF_URL_FMT = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/{doc_id}?type=2'
        pdf_urls = [PDF_URL_FMT.format(doc_id=di) for di in doc_ids]

        return pd.DataFrame({
            'doc_descriptions': doc_descriptions,
            'doc_ids': doc_ids,
            'filer_names': filer_names,
            'period_starts': period_starts,
            'period_ends': period_ends,
            'submit_datetimes': submit_datetimes,
            'pdf_urls': pdf_urls,
        })
