import os
import requests
from time import sleep
from pyquery import PyQuery
from libs import Scraper
from libs import Writer
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
        self.__parser = HtmlParser()
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
                response = requests.get(url=url, headers=self.__headers, proxies=self.__proxies)
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

        ic(__all_url)
        for ind, one_url in enumerate(__all_url):
            ic(ind)
            ic(one_url)
            self.main(url=one_url)

        self.__writer.ex(path=f"data/Results/results.json", content=self.__all_results)

            


if __name__ == '__main__':
    main = Main()
    main.main(url='https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cp_36%3A2421891011&dc&content-id=amzn1.sym.be90cfaf-ddce-4e28-b561-f2a8c0017fef&pd_rd_r=c7b043d7-6715-4eba-8a07-1324ff7b4ddb&pd_rd_w=KK1K8&pd_rd_wg=NZV11&pf_rd_p=be90cfaf-ddce-4e28-b561-f2a8c0017fef&pf_rd_r=E69ZY9ADBEPD57BXZDKD&qid=1702363888&ref=sr_pg_1')