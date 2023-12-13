import json
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
        self.__proxies = {
            "http": "154.6.96.156:3128"
        }
        self.__headers = {
            "session-token": "0012BuKxT3GizFYBS0WTY4vpIdMVePf8Z1wgM6OY++YluvBh6Kz+94kq+NAZ62GIfL5wlpslbpH5gh5yb47i4fvDK7kSusksRd9SgUBC0H0e3KtiyBOaSU2GTSp8kk+8pS/Gq+YBNn2smr0Cpz0t6NiqrSt5sJiFbIwjrnUAffqvz1Gr7jArqt7QC8CCqgdvjbkXVCy0CX6ERceLAR6HhKlQhD/hzPjRYZQCAWFHRt3eEDPcSuEVFbP5UqYCq4OgRp3jCQItWab22/esSNsfvnLweEllKNg5d0QVKHOQvxpfNvZqWuMgA10aUfK8KmEyez3fSxm+fB/9NrdYuRuGakW3KeLVsHCe",
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


    def retry(self, url, max_retries= 5, retry_interval= 0.2) -> PyQuery:
        
        for _ in range(max_retries):
            try:
                response = requests.get(url=url, headers=self.__headers, proxies=self.__proxies)
                ic(retry_interval)
                sleep(retry_interval)
                ic(response)
                html = PyQuery(response.text)
                body = html.find(selector='#dp-container')
                
                if body.find(selector="#productDetails_expanderTables_depthLeftSections > [data-csa-c-content-id='voyager-expander-btn'] > span").length:
                     return body
                
            except requests.RequestException as err:
                 ic(err)
            retry_interval+= 0.2
        return body


    def extract_data(self, url: str):
        
        response = requests.get(url=url, headers=self.__headers, proxies=self.__proxies)
        ic(response)
        html = PyQuery(response.text)
        body = self.retry(url=url)

        table_left = body.find(selector="#productDetails_expanderTables_depthLeftSections > [data-csa-c-content-id='voyager-expander-btn'] > div:nth-child(2)  > div > table")
        table_right = body.find(selector="#productDetails_expanderTables_depthRightSections > [data-csa-c-content-id='voyager-expander-btn'] > div:nth-child(2)  > div > table")

        
        key_left = [self.__parser.ex(html=left, selector='a').text() for left in body.find(selector="#productDetails_expanderTables_depthLeftSections > [data-csa-c-content-id='voyager-expander-btn'] > span")]
        key_right = [self.__parser.ex(html=right, selector='a').text() for right in body.find(selector="#productDetails_expanderTables_depthRightSections > [data-csa-c-content-id='voyager-expander-btn'] > span")]


        product_information: list(dict) = []
        for ind, supplement in enumerate(table_left):
            product_information_left = {
                key_left[ind]: {
                    key.text.strip(): self.__parser.ex(html=supplement, selector="td")[value].text.strip() for value, key in enumerate(self.__parser.ex(html=supplement, selector="tr th:first-child")) if self.__parser.ex(html=supplement, selector="tr th:first-child") != "Customer Reviews"
                } 
            }

            product_information.append(product_information_left)

        for ind, supplement in enumerate(table_right):
            product_information_right = {
                key_right[ind]: {
                    key.text.strip(): self.__parser.ex(html=supplement, selector="td")[value].text.strip() for value, key in enumerate(self.__parser.ex(html=supplement, selector="tr th:first-child"))
                }
            }

            product_information.append(product_information_right)


        # ic(self.__parser.ex(html= body, selector="#productDetails_expanderSectionTables > div > div:nth-child(1) > div.a-row.a-spacing-base > div > div:nth-child(2) > span:nth-child(1))").text())
        # ic(self.__parser.ex(html= body, selector="productDetails_expanderSectionTables > div > div:nth-child(2) > div.a-row.a-spacing-base > div > div:nth-child(2) > span:nth-child(1))").text())

        try:
            if self.__parser.ex(html=body, selector="#productDetails_expanderSectionTables > div > div:first-child > div:nth-child(2) > div"):
                Warranty_and_Support =[ self.__parser.ex(html=span, selector="span").text() for span in self.__parser.ex(html=body, selector="#productDetails_expanderSectionTables > div > div:first-child > div:nth-child(2) > div")]
            else:
                Warranty_and_Support =[ self.__parser.ex(html=span, selector="span").text() for span in self.__parser.ex(html=body, selector="#productDetails_expanderSectionTables > div > div:last-child > div:nth-child(2) > div")]

        except:
            Warranty_and_Support = None


        details = {
            "captions": self.__parser.ex(html=body, selector='#acBadge_feature_div > div > span.ac-for-text > span').text(),
            "bought ": self.__parser.ex(html=body, selector='#social-proofing-faceout-title-tk_bought > span').text(),
            "store": self.__parser.ex(html=body, selector='#bylineInfo').text(),
            "ratings": self.__parser.ex(html=body, selector='#acrCustomerReviewText').text().split(' ')[0],
            "stars": self.__parser.ex(html=body, selector='#acrPopover > span.a-declarative > a > span:first-child').text().split(' ')[0],
            "discount": self.__parser.ex(html=body, selector='#corePriceDisplay_desktop_feature_div > div:nth-child(2) > span:nth-child(2)').text(),
            "price": self.__parser.ex(html=body, selector='#corePriceDisplay_desktop_feature_div > div:nth-child(2) > span:nth-child(3) > span:nth-child(2)').text(),
            "specification": {
               self.__parser.ex(html=spec, selector='td:first-child').text():  self.__parser.ex(html=spec, selector='td:last-child').text() for spec in body.find(selector="#poExpander tr")
            },
            "warranty_and_Support": Warranty_and_Support,
            "product_information": product_information,
            "product_descriptions": self.__parser.ex(html=body, selector="#productDescription > p > span").text()
        } 


        self.__writer.ex(path="private/percobaan12.json", content=details)
        ic(details)




    def ex(self, url_page: str):
        # urls = self.extract_url(url_page=url_page)

        self.extract_data(url="https://www.amazon.com/ASUS-ROG-Strix-Gaming-Laptop/dp/B0BV8H8HVD/ref=sr_1_4?content-id=amzn1.sym.be90cfaf-ddce-4e28-b561-f2a8c0017fef&pd_rd_r=c7b043d7-6715-4eba-8a07-1324ff7b4ddb&pd_rd_w=KK1K8&pd_rd_wg=NZV11&pf_rd_p=be90cfaf-ddce-4e28-b561-f2a8c0017fef&pf_rd_r=E69ZY9ADBEPD57BXZDKD&qid=1702378541&refinements=p_36%3A2421891011&s=electronics&sr=1-4&th=1")
        # for url in urls:
            # break