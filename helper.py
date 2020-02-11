from bs4 import BeautifulSoup
import requests


def readFile(file):
    content = file.read()
    requestForSearchDetails(content)


def requestForSearchDetails(query):
    url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + query
    response = requests.get(url, params=None)
    print(response)
