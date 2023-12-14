from libs import Scraper
from libs import Writer
from icecream import ic
from datetime import datetime as time


class Main:
    def __init__(self) -> None:
        self.__writer = Writer()


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


    def main(self, url: str):
        main_url = self.connect_main_url(url=url)

        all_data = {
            "kategories": "Electronic",
            "times": time.now,
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
                "times": time.now,
                "page": page,
                "datas": results
            }

            self.__writer.ex(path=f"data/page{page}.json", content=page_results)

            page += 1
            if page == 5: break

        

if __name__ == '__main__':
    main = Main()
    main.main(url='https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cp_36%3A2421891011&dc&content-id=amzn1.sym.be90cfaf-ddce-4e28-b561-f2a8c0017fef&pd_rd_r=c7b043d7-6715-4eba-8a07-1324ff7b4ddb&pd_rd_w=KK1K8&pd_rd_wg=NZV11&pf_rd_p=be90cfaf-ddce-4e28-b561-f2a8c0017fef&pf_rd_r=E69ZY9ADBEPD57BXZDKD&qid=1702363888&ref=sr_pg_1')