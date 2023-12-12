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
            "session-token": "wxXMDsC6wPeUPFMuIPOBD8CHUklziBMiYYwQSGgQKmOJwhetjQAc9EQ2cArUarZ0kiY22RVXOC193Bzpn6KJ5PC32kkl1Za7FS7DoCU4N1LqsBgufxdO2WJPLSlfPPIHXrYIaR15FEw6HYBmwXPYgnlLxrexXvJrQ9T4VOrx5aH4ItTaqhzCMp9dHkGOkdQ5uHWNLeGR+NZYyx68zm25E+ihdukW1ZDa05LM/anfRfnktrEuMrrWQ7QrbBxG1lD0mJHwG4YanaonfSzliPD1BPd86v/+iOCwNH4QZ3uwJdvId/+m8RToASD1AnXlxLogUpO52VWVtZAMubcb4flR9vwcHL4jYF2Y",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }


    def filter_url(self, pieces_url: str) -> str:
        return self.__base_url+pieces_url


    def extract_url(self, url_page: str) -> list:
        urls = []
        response = requests.get(url= url_page, headers=self.__headers)
        html = PyQuery(response.text)

        body = html.find(selector='#search > div.s-desktop-width-max.s-desktop-content.s-wide-grid-style-t1.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div')
        
        for ind, link in enumerate(body):
            if ind < 3 or PyQuery(link)('h2 a').attr('href') == None : continue

            self.__results.append({
                "product": PyQuery(link)('h2 a').text(),
                "url": self.filter_url(PyQuery(link)('h2 a').attr('href'))
            })

            urls.append(self.filter_url(pieces_url=PyQuery(link)('h2 a').attr('href')))

        return urls

        


    def extract_data(self, url: str):
        
        response = requests.get(url=url, headers=self.__headers)
        ic(response)
        html = PyQuery(response.text)
        body = html.find(selector='#dp-container')

        details ={
            "captions": self.__parser.ex(html=body, selector='#acBadge_feature_div > div > span.ac-for-text > span').text(),
            "bought ": self.__parser.ex(html=body, selector='#social-proofing-faceout-title-tk_bought > span').text(),
            "store": self.__parser.ex(html=body, selector='#bylineInfo').text(),
            "ratings": int(self.__parser.ex(html=body, selector='#acrCustomerReviewText').text().split(' ')[0]),
            "stars": float(self.__parser.ex(html=body, selector='#acrPopover > span.a-declarative > a > span:first-child').text().split(' ')[0]),
            "discount": self.__parser.ex(html=body, selector='#corePriceDisplay_desktop_feature_div > div:nth-child(2) > span:nth-child(2)').text(),
            "price": self.__parser.ex(html=body, selector='#corePriceDisplay_desktop_feature_div > div:nth-child(2) > span:nth-child(3) > span:nth-child(2)').text(),
            "specification": {
               self.__parser.ex(html=spec, selector='td:first-child').text():  self.__parser.ex(html=spec, selector='td:last-child').text() for spec in body.find(selector="#poExpander tr")
            } 
        } 

        ic(details)
        # for spec in body.find(selector="#poExpander tr"):
        #     ic(self.__parser.ex(html=spec, selector='td:first-child').text())
        #     ic(self.__parser.ex(html=spec, selector='td:last-child').text())
        # ic()

        # self.__writer.exstr(path='private/inner.html', content=str(html))


    def ex(self, url_page: str):
        # urls = self.extract_url(url_page=url_page)

        self.extract_data(url="https://www.amazon.com/ASUS-ROG-Strix-Gaming-Laptop/dp/B0BV8H8HVD/ref=sr_1_4?content-id=amzn1.sym.be90cfaf-ddce-4e28-b561-f2a8c0017fef&pd_rd_r=c7b043d7-6715-4eba-8a07-1324ff7b4ddb&pd_rd_w=KK1K8&pd_rd_wg=NZV11&pf_rd_p=be90cfaf-ddce-4e28-b561-f2a8c0017fef&pf_rd_r=E69ZY9ADBEPD57BXZDKD&qid=1702378541&refinements=p_36%3A2421891011&s=electronics&sr=1-4&th=1")
        # for url in urls:
            # break