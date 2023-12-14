import logging
from datetime import datetime as time

class Logs:
    def __init__(self) -> None:
        pass

    def ex(self, type, title, base_url, child_url) -> None:
        log = f"""
Type: {type}
Title: {title}
Base_url: {base_url}
scrapping_url: {child_url}
Status: success
Time: {time.now()}
            """
        
        print(log)