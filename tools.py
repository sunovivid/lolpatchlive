from datetime import datetime, date
import os
import csv
import json

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getDdVersion():
    return requests.get("https://ddragon.leagueoflegends.com/realms/kr.json").json()["n"]["champion"]

def getDictFromJsonUrl(url):
    fileName = url[url.rfind("/")+1:]
    filePath = os.path.join(os.path.join(BASE_DIR, 'resources'), fileName)
    if os.path.exists(filePath):
        with open(filePath, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
    else:
        data = requests.get(url).json()
        with open(filePath, 'w+', encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent="\t")
    return data

def getChampionJson():
    return getDictFromJsonUrl("http://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/champion.json".format(getDdVersion()))["data"].items()

def getChampionImageUrl(championName):
    championEngName = ''
    for key, value in getChampionJson():
        if championName == value["name"]:
            championEngName = str(key)
    return "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png".format(getDdVersion(),championEngName)

def getLiveClientVersion():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(os.path.join(BASE_DIR,'resources'),'2020 패치 일정.csv'), 'r', encoding='UTF-8') as csvfile:
        rd = list(map(lambda x:(x[0], x[1]),csv.reader(csvfile)))
        for i, (version, dayString) in enumerate(rd):
            if version is not None and dayString is not None:
                #10.1, 2020년 1월 8일 수요일
                patchDate = datetime.strptime(dayString[:-3].strip(), "%Y년 %m월 %d일").date()
                #print(version, patchDate, date.today())
                if date.today() < patchDate:
                    return (rd[i-1])[0]