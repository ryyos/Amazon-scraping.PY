import logging
from datetime import datetime as time

class Logs:
    def __init__(self) -> None:
        # Konfigurasi logging hanya satu kali dalam __init__
        logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', encoding="utf-8", level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        # Membuat handler untuk output ke console (stdout)
        console = logging.StreamHandler()
        console.setLevel(level=logging.INFO)  # Set level ke INFO atau lebih tinggi untuk console handler
        console.setFormatter(formatter)

        # Membuat handler untuk menyimpan log ke file
        file_log = logging.FileHandler(filename="logs/logging.log", encoding="utf-8")
        file_log.setLevel(level=logging.DEBUG)  # Set level ke DEBUG untuk file handler
        file_log.setFormatter(formatter)

        # Menghapus semua handler yang ada sebelum menambahkan yang baru
        logger = logging.getLogger()
        for existing_handler in logger.handlers[:]:
            logger.removeHandler(existing_handler)

        # Menambahkan handler ke logger
        logger.addHandler(console)
        logger.addHandler(file_log)

    def ex(self, status, page, no) -> None:
        logger = logging.getLogger()
        logger.info(f"page: {page}")
        logger.info(f"no: {no}")
        logger.info(f"status: {status}")
