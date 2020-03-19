from urllib.request import urlopen
from time import sleep
import os
import json
import re
import datetime
import pprint
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lolpatchlive.settings")
import django
django.setup()
from django.utils import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import requests

#from .mainApp.models import TempTable
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from updates.models import *
import tools

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ddVersion = tools.getDdVersion()
ddChampionJson = tools.getChampionJson()

def getHtml(url):
    html = urlopen(url)
    return html

def getWebDriver(url, waitingTime=3, mode=None):
    if mode is "debug":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver')
    driver.implicitly_wait(waitingTime)
    driver.get(url)
    return driver

def getHtmlWithHeadlessChrome(url, waitingTime=3, mode=None):
    driver = getWebDriver(url, waitingTime, mode)
    html = driver.page_source
    return html

# def getLiveClientVersion():
#     html = getHtmlWithHeadlessChrome("https://lol.garena.ph/download", 1)
#     bs = BeautifulSoup(html, "html.parser")
#     versionName = bs.body.find("table", {"class": "patches"}).contents[1].contents[0].a.get_text()
#     start = re.compile("Patch").search(versionName).end()
#     if 'Hotfix' in versionName:
#         end = re.compile("Hotfix").search(versionName).start()
#         version = float(versionName[start:end].strip())
#         minorUpdate = int(versionName[re.compile("#").search(versionName).end():].strip())
#     else:
#         version = float(versionName[start:].strip())
#         minorUpdate = 0
#     return version, minorUpdate

def getAllPatchNoteUrlsAndTitles():
    print("getAllPatchNoteUrlsAndTitles 호출")
    print("옵션 설정 시도")
    options = Options()
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                        'geolocation': 2, 'notifications': 2,
                                                        'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                        'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                        'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                        'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)
    #options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    print("옵션 설정 끝")
    print("드라이버 설정")
    driver = webdriver.Chrome('chromedriver',options=options)
    driver.get("https://kr.leagueoflegends.com/ko-kr/news/game-updates/")
    # WebDriverWait.until(driver,EC.presence_of_all_elements_located)
    print("driver.get 수행 완료")
    print("sleep 1 시작")
    sleep(1)
    print("sleep 1 끝")

    try:
        print("패치 노트 탭 버튼 로딩 대기")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//button[@data-value='blt848875bec2cfcf38']")))
        print("sleep 2 시작")
        sleep(2)
        print("sleep 2 끝")
        print("패치 노트 탭 버튼 로딩 완료")
    except TimeoutException:
        return None
    finally:
        print("1초 대기 시작")
        sleep(1)
        print("1초 대기 끝")
        print("패치 노트 탭 클릭 시도")
        driver.find_element_by_xpath("//button[@data-value='blt848875bec2cfcf38']").click()
        print("패치 노트 탭 클릭 완료")

    print("sleep 3 시작")
    sleep(3)
    print("sleep 3 끝")

    try:
        print("while 루프 진입")
        while True:
            print("while 루프 시작점")
            try:
                print("더 불러오기 버튼 로딩 대기")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//button[@class='style__Anchor-xvphg9-0 rhdLx variant-primary style__LoadMoreButton-sc-7ydx7k-5 bgiGYE is-visible']")))
                print("더 불러오기 버튼 로딩 완료")
            finally:
                print("1초 대기 시작")
                sleep(1)
                print("1초 대기 끝")
                print("더 불러오기 버튼 finally")
                try:
                    print("더 불러오기 버튼 클릭 시도")
                    driver.find_element_by_xpath(
                    "//button[@class='style__Anchor-xvphg9-0 rhdLx variant-primary style__LoadMoreButton-sc-7ydx7k-5 bgiGYE is-visible']").click()
                    print("더 불러오기 버튼 클릭 성공")
                except ElementClickInterceptedException:
                    print(ElementClickInterceptedException)
                    return None
    except TimeoutException:
        print(TimeoutException)
    except NoSuchElementException:
        print(NoSuchElementException)

    try:
        print("리스트 로딩 대기")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ol[@class='style__List-sc-3mnuh-2 dlMnhX']")))
        print("리스트 로딩 완료")
    finally:
        print("1초 대기 시작")
        sleep(1)
        print("1초 대기 끝")
        print("리스트 타이틀, url 추출")
        result =  list(map(
                    lambda x: (x.find_element_by_tag_name("a").get_property("href"), x.find_element_by_tag_name("h2").text),
                    driver.find_elements_by_xpath("//li[@class='style__Item-sc-3mnuh-3 ekxbJn']")
                )) #return URL, TITLE
        driver.quit()
        return result

def checkNewPatchNote():
    try:
        with open(os.path.join('resources','prevTitles.txt'), 'rb') as f:
            prevUrlAndTitles = pickle.load(f)
    except FileNotFoundError:
        with open(os.path.join('resources','prevTitles.txt'), 'wb') as f:
            pickle.dump([], f)
            prevUrlAndTitles = []
    pprint.pprint(prevUrlAndTitles)
    currentUrlsAndTitles = reversed(getAllPatchNoteUrlsAndTitles())
    pprint.pprint(currentUrlsAndTitles)
    while currentUrlsAndTitles is None:
        currentUrlsAndTitles = reversed(getAllPatchNoteUrlsAndTitles())

    for url, title in currentUrlsAndTitles:
        if title not in map(lambda x:x[1], prevUrlAndTitles):
            print("getPatchNote({})".format(title))
            getPatchNote(url)
    #중간에 getPatchNote가 실패하고 타이틀만 저장하는 경우를 막기 위해 파일을 나중에 저장
    with open(os.path.join('resources','prevTitles.txt'),'wb') as f:
        pickle.dump(currentUrlsAndTitles, f)

def parseTitle(title):
    end = re.compile("패치 노트").search(title).start()
    start = 0
    minorUpdate = 0
    if '[#' in title:
        start = re.compile("\[#\d\]").search(title).end()
        minorUpdate = int(title[title.find('[#')+2:title.find(']')])
    version = str(title[start:end].strip())
    return version, minorUpdate

def isChampion(name):
    for key, value in ddChampionJson:
        if name == value["name"]:
            return True
    return False

def getPatchNote(url, getMinorUpdateOnly=False):

    def getAndSaveModelSafe(Model, **kwargs):
        model, isCreated = Model.objects.get_or_create(**kwargs)
        if isCreated:
            model.save()
            print("모델 저장 성공 {}".format(str(Model)))
        else:
            print("이미 저장된 모델 {}".format(str(Model)))
        return model


    html = getHtml(url)
    bs = BeautifulSoup(html, "lxml")

    title = bs.find("h1", {"class": "style__Title-sc-1p3d5t5-5 fCQbDk"}).get_text() #title example: [#3] 10.5 패치 노트 (수정)
    version, minorUpdate = parseTitle(title)

    # 파싱해서 섹션으로 구조화
    sampleData = {
        "version":10.4,
        "summary":"이번 패치에서는 공격로에서 압도적인 위력을 보여주고 있는 상단 공격로 소나와 소라카의 위력을 저지하려고 합니다. ",
        "headers": {
            "추가 패치 노트": {
                "2020년 2월 22일 탐 켄치 버그 수정": {
                    "탐 켄치": [
                        "W - 집어삼키기 버그 수정 탐 켄치가 W - 집어삼키기로 집어삼킨 아군을 자신의 앞으로 뱉어내지 못하는 문제가 수정되었습니다."
                    ]
                },
                "2020년 2월 21일 티아맷/굶주린 히드라 버그 수정 및 불사르기 아이템, 소나, 소라카 밸런스 조정": {
                    "뽀삐": [
                        "티아맷/굶주린 히드라 버그 수정 뽀삐가 원거리에서도 티아맷과 굶주린 히드라의 사용 효과를 발동시킬 수 있었던 문제가 수정되었습니다."
                    ],
                    "소나": [
                        "기본 공격력 49 ⇒ 45",
                        "E - 기민함의 노래 소나 이동 속도 증가 20% (+주문력 100당 3%) ⇒ 10/11/12/13/14% (+주문력 100당 3%)"
                    ]
                }
            },
            "패치 하이라이트": {
                "불의 축제 트린다미어, 불의 축제 카타리나, 불의 축제 마스터 이가 이번 패치 기간 중 출시됩니다."
            },
            "챔피언": {
                "아무무": {
                    "summary":"Q - 붕대 던지기의 돌진 속도가 증가합니다. R - 슬픈 미라의 저주 재사용 대기시간이 감소하고 이제 돌진하는 적을 멈춥니다.",
                    "quote":"이번 상향은 아래에서 확인하실 수 있는 10.4 패치 불사르기 변경사항과 함께 아무무의 위력에 도움이 될 겁니다.",
                    "htmlsource":"<div>...</div>"
                },
                "아펠리오스": {

                }
            },
            "정글 챔피언": [
                "<div></div>"
            ],
            "상단 공격로의 중요성": [
                "<div></div>",
                "<div></div>"
            ]
            #확인하지 못한 분들을 위한.., 버그 수정 뒤 내용, 앞으로 나올 스킨 및 크로마, 시각 효과 및 음향 효과 업데이트는 제외
            #챔피언, 추가 패치 노트, *아이템 헤더만 특별 취급, 나머지는 article 단위로 일단은 html소스만
            #이후 타이틀(존재시), 인용(존재시)까지 저장은 생각해보자
        }

    }
    data = {"version":version, "headers":{}, "models":{}}
    summary = ""
    header = ""
    versionModel = None
    headerModel = None
    MINOR_UPDATE_DEFAULT = "아직 추가 패치 노트 없음"
    lastMinorUpdateTitle = MINOR_UPDATE_DEFAULT

    def articleSave(content, header, headerModel):
        print('\t<아티클>',header)
        contentHtml = content.find("div", {"class": "patch-change-block white-stone accent-before"})
        data["headers"][header].append(contentHtml)
        articleModel = getAndSaveModelSafe(ArticleModel, contentHtml=str(contentHtml), header=headerModel)


    def initVersionSetting(versionModel):
        minorModelsForThisVersion = MinorUpdateModel.objects.filter(version=versionModel).order_by(
            '-updateDate')
        if not minorModelsForThisVersion.exists():
            lastMinorUpdateModel = getAndSaveModelSafe(MinorUpdateModel, updateTitle=MINOR_UPDATE_DEFAULT,
                                                       version=versionModel)
        else:
            lastMinorUpdateModel = minorModelsForThisVersion[0]
        lastMinorUpdateTitle = lastMinorUpdateModel.updateTitle

    isVersionSettingInitiated = False
    for content in bs.find("div", {"id": "patch-notes-container"}).children:
        if content.name is not None:
            if content.name == "blockquote":
                summary = content.get_text().strip()
                data["summary"] = summary
                versionModel = getAndSaveModelSafe(VersionModel, version=str(version), summary=summary)
                if not isVersionSettingInitiated:
                    initVersionSetting(versionModel)
                    isVersionSettingInitiated = True
            elif content.name == "header":
                header = content.get_text().strip()
                data["headers"][header] = []
                headerModel = getAndSaveModelSafe(HeaderModel, header=header, version=versionModel)
                print("<새 헤더> "+header)
                if header == "추가 패치 노트":
                    data["models"]["추가 패치 노트"] = {}
                elif header == "챔피언":
                    data["models"]["챔피언"] = {}
            elif content.name == 'div' and content.attrs['class'] == ['content-border']:
                if header == "추가 패치 노트":
                    updateTitle = content.h3.get_text()
                    if updateTitle == lastMinorUpdateTitle:
                        data["models"]["추가 패치 노트"][updateTitle] = "이미 저장한 추가 패치 노트"
                        print("이미 저장한 추가 패치 노트: "+updateTitle)
                        print("최신 버전임")
                        break #디버그할때는 주석처리하기
                    else:
                        print("저장 시도: " + updateTitle)
                        if updateTitle not in map(lambda x:x.updateTitle, MinorUpdateModel.objects.filter(version=versionModel)):
                            data["models"]["추가 패치 노트"][updateTitle] = {}
                            minorUpdateModel = getAndSaveModelSafe(MinorUpdateModel, updateTitle=updateTitle, version=versionModel)
                            for line in content.find("div",{"class":"white-stone accent-before"}).div.children:
                                if line.name is not None:
                                    itemName = "Unnamed item"
                                    data["models"]["추가 패치 노트"][updateTitle][itemName] = []
                                    if line.name == "h4":
                                        itemName = line.get_text().strip()
                                        # item = []
                                        data["models"]["추가 패치 노트"][updateTitle][itemName] = []
                                    elif line.name == "div":
                                        # item.append(str(line))
                                        data["models"]["추가 패치 노트"][updateTitle][itemName].append(str(line))
                            for (itemName, itemList) in data["models"]["추가 패치 노트"][updateTitle].items():
                                if isChampion(itemName):
                                    getAndSaveModelSafe(ChampionMinorPatchModel, championName=itemName,
                                                        contentHtmlList=str(itemList),
                                                        minorUpdate=minorUpdateModel)
                                getAndSaveModelSafe(MinorUpdateItemModel, itemName=itemName, item=str(itemList),
                                                    minorUpdate=minorUpdateModel, updateDate=timezone.now())
                            print("저장 완료: "+updateTitle)
                        else:
                            print("저장할 필요 없음: " + updateTitle)
                elif not getMinorUpdateOnly:
                    print("getMinorUpdateOnly")
                    articleSave(content, header, headerModel)
                    if header == "챔피언":
                        championName = content.div.div.h3.a.get_text()
                        data["models"]["챔피언"][championName] = {}
                        championSummary = content.div.div.find("p", {"class": "summary"})
                        if championSummary is not None:
                            championSummaryText = championSummary.get_text()
                        else:
                            championSummaryText = ''
                        data["models"]["챔피언"][championName]["summary"] = championSummaryText
                        quote = content.div.div.find("blockquote", {"class": "blockquote context"})
                        if quote is not None:
                            quoteText = quote.get_text()
                        else:
                            quoteText = ''
                        data["models"]["챔피언"][championName]["quote"] = quoteText
                        contentHtml = content.find("div", {"class": "patch-change-block white-stone accent-before"})
                        if contentHtml is not None:
                            contentHtml = str(contentHtml)
                        else:
                            contentHtml = '404 error'
                        data["models"]["챔피언"][championName]["html"] = str(contentHtml)
                        print("\t[챔피언] "+championName+": "+championSummaryText)
                        championPatchModel = getAndSaveModelSafe(ChampionPatchModel, championName=championName,championSummaryText=championSummaryText,championQuoteText=quoteText,contentHtml=contentHtml,version=versionModel)
            else:
                if content.get_text() != '맨 위로 돌아가기':
                    print("<UNKNOWN TAG ERROR>" + str(content))
    if summary is None:
        print("THERE IS NO SUMMARY ERROR")

    # def formTree(list):
    #     tree = {}
    #     for item in list:
    #         currTree = tree
    #
    #         for key in item[::-1]:
    #             if key not in currTree:
    #                 currTree[key] = {}
    #             currTree = currTree[key]
    #     return tree
    # def dictionarize(currDict):
    #     newDict = {}
    #     for key, value in currDict.items():
    #         if type(value) == "<class 'list'>":
    #             newDict[key] = dict(value)
    #         elif type(value) == "<class 'dict'>":
    #             newDict[key] = dictionarize(value)
    #         else:
    #             newDict[key] = value
    #     return newDict

    #pprint.pprint(data,indent=2)
    # with open(os.path.join(os.path.join(BASE_DIR,"log"), str("ver"+str(version)+" "+str(timezone.now().strftime("%Y-%m-%d %H-%M-%S"))+'.json')), 'w+', encoding="utf-8") as json_file:
    #     json.dump(dictionarize(data), json_file, ensure_ascii=False, indent="\t")

if __name__ == '__main__':
    def getAllPatchNoteFromPrevUrls():
        try:
            print("File Found")
            with open(os.path.join('resources', 'prevTitles.txt'), 'rb') as f:
                prevUrlAndTitles = pickle.load(f)
        except FileNotFoundError:
            print("File Not Found")
            with open(os.path.join('resources', 'prevTitles.txt'), 'wb') as f:
                pickle.dump([], f)
                prevUrlAndTitles = []
        pprint.pprint(prevUrlAndTitles)
        for url, title in prevUrlAndTitles:
            title = title.strip()
            if title not in map(lambda x: x[1], prevUrlAndTitles):
                print("getPatchNote({})".format(title))
                getPatchNote(url)


    #getAllPatchNoteFromPrevUrls()
    checkNewPatchNote()
    #getPatchNote("https://kr.leagueoflegends.com/ko-kr/news/game-updates/9-18-paechi-noteu-sujeong/")