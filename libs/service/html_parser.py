import json
import requests
from time import sleep
from pyquery import PyQuery
from icecream import ic
from libs.utils.parser import HtmlParser
from libs.utils.writer import Writer
from libs.utils.logs import Logs

class Scraper:
    def __init__(self) -> None:
        self.__parser = HtmlParser()
        self.__writer = Writer()
        self.__logs = Logs()
        self.__results: list(dict) = []
        self.__status_code = None
        self.__base_url = 'https://www.amazon.com'
        self.__proxies = {
            "http": "154.6.96.156:3128"
        }
        self.__headers = {
            "session-id": "145-8749830-8342303",
            "session-id-time": "2082787201l",
            "session-token": "mfmMRa1ybjsrNTLOszvuJ2WptU3jvimRQdF6BwgelKa8QOivSUkh/efayFPrbVT+hdVv4eakclN6S42zeNKmFcE+2KXypTA/H0JMNQ/TJtwAojie34SJTBcBqLIeS7Y+b4zqU5efcHFHWTY0Lrw4GO+z0fNPQsegzHNdJPPM7sZwiJyi9u8dhIaZMelC2cUj6YQd/gozXTpT2fKSu1KSk7ORONo7xfQiCGEqYuJzcD2TXXMeNhaYDVf+jTdfIkjTPqVLrN09IEt2+XaBC+eVaszRwXFKx/3uXJ6/14L+W6mhmMfEGjZkwAp3++1QInb4pejfTGMzWpUKXdhJLzHaK3hlB40G2glu",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def retry(self, url, max_retries= 5, retry_interval= 0.2):
        for _ in range(max_retries):
            try:
                response = requests.get(url=url, headers=self.__headers, proxies=self.__proxies)
                if response.status_code == 200: return response
            except requests.RequestException as err:
                 ic(err)
            retry_interval+= 0.2
        return response


    def filter_url(self, pieces_url: str) -> str:
        return self.__base_url+pieces_url


    def __filter_str(self, text: str) -> str:
        return text.replace('\"', "'")\
            .replace("\u2019", "'")\
            .replace("\uff1a", "")\
            .replace('\n', '')\
            .replace('\"', "'")\
            .replace("\u2011", '')\
            .replace("\u00d7", '')\
            .replace("\u201c", '')\
            .replace("\u202f", '')\
            .replace("\u03b1", '')\
            .replace("\u00b0", '')\
            .replace("\u2122", '')\
            .replace("\uff01", '')\
            .replace("\u2013", '')\
            .replace("\u00ae", '')\
            .replace("\u201d", "")\
            .replace("\u00a0", "")\
            .replace("\u2014", "")\
            .split(";")[-1]



    def extract_url(self, url_page: str) -> list:
        urls = []
        try:
            response = requests.get(url= url_page, headers=self.__headers)
            ic(response)
        except requests.ConnectionError as err:
            response = self.retry(url=url_page, max_retries=5)
        
        html = PyQuery(response.text)

        body = html.find(selector='#search > div.s-desktop-width-max.s-desktop-content.s-wide-grid-style-t1.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div')
        for ind, link in enumerate(body):
            if ind < 3 or PyQuery(link)('h2 a').attr('href') == None : continue

            self.__results.append({
                "product": self.__filter_str(PyQuery(link)('h2 a').text()),
                "url": self.filter_url(PyQuery(link)('h2 a').attr('href'))
            })

            urls.append(self.filter_url(pieces_url=PyQuery(link)('h2 a').attr('href')))

        return urls

    def extract_data(self, url: str):

        try:
            response = self.retry(url=url)
            self.__status_code = response.status_code
        except requests.ConnectTimeout as err:
            self.__status_code = err
            response = self.retry(url=url)

        html = PyQuery(response.text)
        body = html.find(selector='#dp-container')

        table_left = body.find(selector="#productDetails_expanderTables_depthLeftSections > [data-csa-c-content-id='voyager-expander-btn'] > div:nth-child(2)  > div > table")
        table_right = body.find(selector="#productDetails_expanderTables_depthRightSections > [data-csa-c-content-id='voyager-expander-btn'] > div:nth-child(2)  > div > table")

        mac_table_left = body.find(selector="#btfContent31_feature_div > div > div:nth-child(3) > div:first-child > div:first-child > div:nth-child(1) > table > tr") 
        mac_table_right = body.find(selector="#btfContent31_feature_div > div > div:nth-child(3) > div:first-child > div:last-child > div:nth-child(1) > table > tr") 

        can_table = body.find(selector="#productDetails_detailBullets_sections1 tr")
        graphic_table = body.find(selector="#productDetails_techSpec_section_1 tr")

        key_left = [self.__parser.ex(html=left, selector='a').text() for left in body.find(selector="#productDetails_expanderTables_depthLeftSections > [data-csa-c-content-id='voyager-expander-btn'] > span")]
        key_right = [self.__parser.ex(html=right, selector='a').text() for right in body.find(selector="#productDetails_expanderTables_depthRightSections > [data-csa-c-content-id='voyager-expander-btn'] > span")]

        spesifications = body.find(selector="#poExpander tr")
        Warranty_and_Support = [ self.__filter_str(self.__parser.ex(html=span, selector="span").text()) for span in self.__parser.ex(html=body, selector="#productDetails_expanderSectionTables > div > div:first-child > div:nth-child(2) > div")]

        product_information: list(dict) = []

        if not spesifications:
            spesifications = body.find(selector="#productOverview_feature_div > div > table > tr")
        

        for ind, supplement in enumerate(table_left):
            product_information_left = {
                key_left[ind]: {
                    key.text.strip():self.__filter_str(self.__parser.ex(html=supplement, selector="td")[value].text.strip()) for value, key in enumerate(self.__parser.ex(html=supplement, selector="tr th:first-child"))
                } 
            }

            product_information.append(product_information_left)

        for ind, supplement in enumerate(table_right):
            product_information_right = {
                key_right[ind]: {
                    key.text.strip(): self.__filter_str(self.__parser.ex(html=supplement, selector="td")[value].text.strip()) for value, key in enumerate(self.__parser.ex(html=supplement, selector="tr th:first-child"))
                }
            }

            product_information.append(product_information_right)

        if not product_information:
            product = {}
            product.update({
                self.__parser.ex(html=supplement, selector="td:first-child").text(): self.__parser.ex(html=supplement, selector="td:first-child").text() for supplement in mac_table_left
            })
            product.update({
                self.__parser.ex(html=supplement, selector="td:first-child").text(): self.__parser.ex(html=supplement, selector="td:last-child").text() for supplement in mac_table_right
            })

            if bool(product): product_information.append(product)

        if not product_information:
            product = {}
            product.update({
                self.__parser.ex(html=can, selector="th").text(): self.__filter_str(text=self.__parser.ex(html=can, selector="td").text()) for can in can_table
            })

            if bool(product): product_information.append(product)

        if not product_information:
            product = {}
            product.update({
                self.__parser.ex(html=graphic, selector="th").text(): self.__filter_str(text=self.__parser.ex(html=graphic, selector="td").text()) for graphic in graphic_table
            })

            if bool(product): product_information.append(product)

        

        if not Warranty_and_Support:
            Warranty_and_Support =[ self.filter_url(self.__parser.ex(html=span, selector="span").text()) for span in self.__parser.ex(html=body, selector="#productDetails_expanderSectionTables > div > div:last-child > div:nth-child(2) > div")]


        details = {
            "captions": self.__parser.ex(html=body, selector='#acBadge_feature_div > div > span.ac-for-text > span').text(),
            "bought ": self.__parser.ex(html=body, selector='#social-proofing-faceout-title-tk_bought > span').text(),
            "store": self.__parser.ex(html=body, selector='#bylineInfo').text(),
            "ratings": self.__parser.ex(html=body, selector='#acrCustomerReviewText').text().split(' ')[0],
            "stars": self.__parser.ex(html=body, selector='#acrPopover > span.a-declarative > a > span:first-child').text().split(' ')[0],
            "discount": self.__parser.ex(html=body, selector='#corePriceDisplay_desktop_feature_div > div:nth-child(2) > span:nth-child(2)').text(),
            "price": self.__parser.ex(html=body, selector='#corePriceDisplay_desktop_feature_div > div:nth-child(2) > span:nth-child(3) > span:nth-child(2)').text(),
            "about_this_item": [self.__filter_str(self.__parser.ex(html=about, selector="span").text()) for about in body.find(selector="#feature-bullets > ul > li")],
            "specification": {
               self.__filter_str(text=self.__parser.ex(html=spec, selector='td:first-child').text()):  self.__filter_str(text=self.__parser.ex(html=spec, selector='td:last-child').text()) for spec in spesifications
            },
            "warranty_and_Support": Warranty_and_Support,
            "product_information": product_information,
            "product_descriptions": self.__filter_str(self.__parser.ex(html=body, selector="#productDescription > p > span").text())
        } 


        # self.__writer.ex(path=f"private/percobaan23.json", content=details)

        return details


    def ex(self, page: int,  url_page: str):
        urls = self.extract_url(url_page=url_page)

        if not urls: return "clear"

        # self.extract_data(url="https://www.amazon.com/Canon-USA-3680C002-24-70mm-F2-8/dp/B07WQ54BL8/ref=sr_1_18?content-id=amzn1.sym.be90cfaf-ddce-4e28-b561-f2a8c0017fef&pd_rd_r=c7b043d7-6715-4eba-8a07-1324ff7b4ddb&pd_rd_w=KK1K8&pd_rd_wg=NZV11&pf_rd_p=be90cfaf-ddce-4e28-b561-f2a8c0017fef&pf_rd_r=E69ZY9ADBEPD57BXZDKD&qid=1702491782&refinements=p_36%3A2421891011&s=electronics&sr=1-18")
        for ind, url in enumerate(urls):
            self.__results[ind].update({"no": ind+1})
            self.__results[ind].update({
                "details": self.extract_data(url=url)
            })
            self.__logs.ex(status=self.__status_code, page=page, no=ind)
        
        return self.__results