import click
import configparser
import json
import requests
from bs4 import BeautifulSoup

# configuration things
settings = configparser.ConfigParser()
settings.read("config.ini")

SEARCH_URL = settings.get("TimeEdit", "SearchUrl")
TYPE = settings.get("TimeEdit", "Type")
SCHEDULE_URL = settings.get("TimeEdit", "ScheduleUrl")

# header
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def getUrl(courseCode): 
    html = ""

    try:
        html = requests.get(SEARCH_URL + courseCode + TYPE, headers=HEADERS)
    except requests.ConnectionError:
        click.echo("Err: No Internet Connection!")
        exit(0) 
    
    return BeautifulSoup(html.content, "html.parser")

def parseUrl(soup):
    div = soup.find("div", {"id": "objectbasketitemX0"})
    dataId = div["data-id"]
    return dataId

def getSchedule(courseCode, weeks):
    dataId = parseUrl(getUrl(courseCode))
    json = ""
    
    # build url who request schedule
    url = SCHEDULE_URL + weeks + ".w" + "&objects=" + dataId
    
    try:
        json = requests.get(url, headers=HEADERS)
    except requests.ConnectionError:
        click.echo("Err: No Internet Connection!")
        exit(0)

    return json.content

def parseJson(jsonString):
    parsedJson = json.loads(jsonString.decode("utf-8"))
    
    result = []

    for reservation in parsedJson["reservations"]:
        columns = []

        columns.append(reservation["startdate"] + ", " + reservation["starttime"] +
                    " - " + reservation["endtime"])

        for column in reservation["columns"]:
            columns.append(column)
        
        result.append(columns)

    return result















