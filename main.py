import os
import requests
from time import sleep
from pyquery import PyQuery
from libs import Scraper
from libs import Writer
from fake_useragent import UserAgent
from libs import HtmlParser
from icecream import ic
from datetime import datetime as time


class Main:
    def __init__(self) -> None:
        os.mkdir("data/Results")
        self.__all_results: list(dict) = []
        self.__all_urls = []
        self.__all_categories: str = []
        self.__writer = Writer()
        self.__user_agent = UserAgent()
        self.__parser = HtmlParser()
        self.__base_url = 'https://www.amazon.com'
        self.__proxies = {
            "http": "154.6.96.156:3128"
        }
        self.__headers = {
            "session-token": "8SG7IBG+BKYH9gc+2on4mz/+64QqtKjJYcV1/6enxbCesEGVJ4+9p/HDKef9q3sB3d/nhFYVWwoCXsNGf7TO/k5EeduOoGh8WjZaVHkRGYFWAZSjIu/uQ0dt/R4LrTZxb7oaROD6Avl323INUhPAiPvU8S+UDz01CrTY810WXgyDZ8lMXs+QPPFnQGlA2fWDqcO7EtiVTFyZ8rZMNggE544gdQU/5jL27xgMMYY3tssLTkiMOe59mVXZcxCaVgHUYzu5gL6Xw0XbqshSGXXloq4132Vc8wX936KEBLkoNx+wTdaqZJJNvOf8yxSlEWgnNZ7m1Y6iHxGQUHgmHtBnHsPmZTmgSail",
            "User-Agent": self.__user_agent.random
        }

    def connect_main_url(self, url: str) -> str:
        pieces_url = url.split("&")

        if "page" not in pieces_url:
            pieces_url.append("page=2")

        return "&".join(pieces_url)


    def create_url_page(self, main_url: str, page: str) -> str:
        pieces_url = main_url.split("&")

        for i in range(len(pieces_url)):
            if "page=" in pieces_url[i]:
                pieces_url[i] = f"page={page}"

            if "ref=" in pieces_url[i] :
                pieces_url[i] = f"ref=sr_pg_{page}"
        
        return "&".join(pieces_url)
    

    def retry(self, url, max_retries= 3, retry_interval= 0.2):
        for _ in range(max_retries):
            try:
                response = requests.get(url=url, headers=self.__headers)
                ic(response)
                if response.status_code == 200: return response
            except requests.RequestException as err:
                 ic(err)
            retry_interval+= 0.2
        return response


    def main(self, url: str):
        __all_url = []
        response = self.retry(url=url, max_retries=5)
        body = PyQuery(response.text)

        sides = body.find(selector="#departments > ul > span > li > span")

        main_url = url
        for ind, side in enumerate(sides.items()):
            
            categories = side.text()

            if self.__parser.ex(html=side, selector="a").attr('href') and categories not in self.__all_categories: 
                main_url = self.connect_main_url(url=self.__base_url+self.__parser.ex(html=side, selector="a").attr('href'))
                __all_url.append(main_url)
                
                
                os.mkdir(f"data/{categories.replace(" ", "_")}")
                os.mkdir(f"data/{categories.replace(" ", "_")}/page")
                os.mkdir(f"data/{categories.replace(" ", "_")}/all")

                all_data = {
                    "kategories": categories,
                    "times": str(time.now()),
                    "datas": []
                }

                page = 1
                while True:
                    __scraper = Scraper()
                    url = self.create_url_page(main_url=main_url, page=str(page))

                    results = __scraper.ex(url_page=url, page=page)
                    if results == "clear": break

                    all_data["datas"].append(results)
                    all_data["total_page"] = page

                    page_results = {
                        "kategories": "Electronic",
                        "times": str(time.now()),
                        "page": page,
                        "datas": results
                    }

                    self.__writer.ex(path=f"data/{categories.replace(" ", "_")}/page/page{page}.json", content=page_results)
                    self.__writer.ex(path=f"private/percobaan_link1.json", content=url)

                    page += 1

                self.__writer.ex(path=f"data/{categories.replace(" ", "_")}/all/results.json", content=all_data)
                self.__all_results.append(all_data)

            if categories not in self.__all_categories:
                self.__all_categories.append(categories)

        for ind, one_url in enumerate(__all_url):
            self.main(url=one_url)

        self.__writer.ex(path=f"data/Results/results.json", content=self.__all_results)

            


if __name__ == '__main__':
    main = Main()
    main.main(url='https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cp_36%3A2421891011&dc&content-id=amzn1.sym.be90cfaf-ddce-4e28-b561-f2a8c0017fef&pd_rd_r=c7b043d7-6715-4eba-8a07-1324ff7b4ddb&pd_rd_w=KK1K8&pd_rd_wg=NZV11&pf_rd_p=be90cfaf-ddce-4e28-b561-f2a8c0017fef&pf_rd_r=E69ZY9ADBEPD57BXZDKD&qid=1702363888&ref=sr_pg_1')