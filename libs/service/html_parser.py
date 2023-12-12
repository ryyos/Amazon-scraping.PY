import requests
from time import sleep
from pyquery import PyQuery
from icecream import ic
from libs.utils.parser import HtmlParser
from libs.utils.writer import Writer

class Scraper:
    def __init__(self) -> None:
        self.__parser = HtmlParser()
        self.__writer = Writer()
        self.__results: list(dict) = []
        self.__base_url = 'https://www.amazon.com'
        self.__headers = {
            "session-token": "ispIU1OCEYjZIMFXfS8QORzlADO+tGYk1gWHtm1kOmowNzNL2NdGS580lgSsRV/eGiNnI1MgTAmtcLSLwDtPlOie7fZftdF3ANsnH77+2Ywl/D/EzroFmDzvCDvv0HzSyygM0iv2Y9PCuqKl20tSSJ4M/lA4OqB9JA4fqwnUrDg+TOvj6dch48vynJATxPd5pfHZbA+jHu5qVeNPaWserO3SYn/6cob6/oe0qmp+936NU2OQDsKLkHleCtp7HaijbMObqgz6M3ctW9VMVL5Ft4Pd8OA0nZP24xe5mgXFSIy/KpjtNXmJVwkzYTP8NudkZLTTsbFeyfWzZm+v6OYLw3p3DjvXknWR",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }


    def filter_url(self, pieces_url: str) -> str:
        return self.__base_url+pieces_url


    def extract_url(self, url_page: str):
        response = requests.get(url= url_page)
        html = PyQuery(response.text)

        body = html.find(selector='#search > div.s-desktop-width-max.s-desktop-content.s-wide-grid-style-t1.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div')
        
        for ind, link in enumerate(body):
            if ind < 3: continue

            self.__results.append({
                "product": PyQuery(link)('h2 a').text(),
                "url": self.filter_url(PyQuery(link)('h2 a').attr('href'))
            })


    def extract_data(self, url: str):

        response = requests.get(url=url, headers=self.__headers)
        ic(response)
        html = PyQuery(response.text)
        body = html.find(selector='#search > div.s-desktop-width-max.s-desktop-content.s-wide-grid-style-t1.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div')
        ic(len(body))
        for ind, link in enumerate(body):
            if ind < 3: continue
            ic(PyQuery(link)('h2 a').text())
            ic(self.filter_url(PyQuery(link)('h2 a').attr('href')))
            sleep(5)
            # self.__writer.exstr(path='private/data.html', content=link.text)



        pass
