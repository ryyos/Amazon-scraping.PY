<h1 align="center" >Hello 👋, I'm Ryo</h1>
<h3 align="center" >An independent backend developer</h3>

<h1 align="center" >Welcome To Amazon-Scraping.PY🛍️</h1>

> This program is my training project for scraping data from Amazone's website

## Feature

- The program enables to retrieve all data with electronic categories
- use logs from the logging library so that it can store request logs and response status from the API
- Use function retry to handle when getting a request timeout error
- Use of fake_useragent libraries to avoid 503 or full traffic response codes
- Use of PyQuery library for HTML parsing so that the use of selectors becomes easier
- Using the Icecream library makes it easier to debuggin

## Tech

- [requests](https://docs.python-requests.org/) is an easy-to-use Python library for interacting with APIs and making HTTP requests
- [pyquery](https://pythonhosted.org/pyquery/) is a Python library that allows HTML and XML manipulation with a syntax similar to jQuery
- [fake_useragent](https://pypi.org/project/fake-useragent/) is a Python library that provides an easy way to generate fake user-agent strings for HTTP requests
- [icecream](https://github.com/gruns/icecream) is a Python library that provides a simple and informative way to log code, helping with monitoring program execution flows.

## Requirement

- [Python](https://www.python.org/) v3.12.0
- [Pyquery](https://pythonhosted.org/pyquery/) v2.0.0
- [icecream](https://github.com/gruns/icecream) v2.1.3
- [fake_useragent](https://pypi.org/project/fake-useragent/) v1.4.0
- [requests](https://docs.python-requests.org/) 2.31.0

## Installation

> To run this program you need to install some libraries with the command

```sh
pip install pyquery icecream fake_useragent
```

## Example Usage

```bash
# Clone this repositories
git clone https://github.com/ryosoraa/Amazon-scraping.PY.git

# go into the directory
cd Amazon-scraping.PY

# Run code
python main.py
```

## 🚀Structure

```
│   LICENSE
│   main.py
│   README.md
│
├───data
│   ├───Camera_&_Photo
│   │   ├───all
│   │   └───page
│   │
│   ├───Electronics_Accessories_&_Supplies
│   │   ├───all
│   │   └───page
│   │
│   └───Results
├───libs
│   │   __init__.py
│   │
│   ├───service
│   │   │   html_parser.py
│   │   │
│   │   └───__pycache__
│   │           html_parser.cpython-312.pyc
│   │
│   ├───utils
│   │   │   logs.py
│   │   │   parser.py
│   │   │   writer.py
│   │   │
│   │   └───__pycache__
│   │
│   └───__pycache__
│
├───logs
│       logging.log
```

## Author

👤 **Rio Dwi Saputra**

- Twitter: [@ryosora12](https://twitter.com/ryosora12)
- Github: [@ryosoraa](https://github.com/ryosoraa)
- LinkedIn: [@rio-dwi-saputra-23560b287](https://www.linkedin.com/in/rio-dwi-saputra-23560b287/)

<a href="https://www.linkedin.com/in/ryosora/">
  <img align="left" alt="Ryo's LinkedIn" width="24px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />
</a>
<a href="https://www.instagram.com/ryosoraaa/">
  <img align="left" alt="Ryo's Instagram" width="24px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/instagram.svg" /> 
</a>
