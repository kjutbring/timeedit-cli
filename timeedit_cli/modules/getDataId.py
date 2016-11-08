import click
import requests
from bs4 import BeautifulSoup

URL = "https://se.timeedit.net/web/lu/db1/ht3/objects.html?max=15&fr=t&partajax=t&im=f&sid=5&l=sv_SE&search_text="
TYPE = "&types=183"

def getUrl(Url, courseCode, sType): 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    html = ""

    try:
        html = requests.get(Url + courseCode + sType, headers=headers)
    except requests.ConnectionError:
        click.echo("Err: No Internet Connection!")
        exit(0) 
    
    return BeautifulSoup(html.content, "html.parser")

def parseUrl(soup):
    div = soup.find("div", {"id": "objectbasketitemX0"})
    dataId = div["data-id"]
    return dataId

