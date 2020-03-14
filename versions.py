from datetime import datetime, date
import os
import csv

def getLiveClientVersion():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(os.path.join(BASE_DIR,'resources'),'2020 패치 일정.csv'), 'r', encoding='UTF-8') as csvfile:
        rd = list(map(lambda x:(x[0], x[1]),csv.reader(csvfile)))
        for i, (version, dayString) in enumerate(rd):
            if version is not None and dayString is not None:
                #10.1, 2020년 1월 8일 수요일
                patchDate = datetime.strptime(dayString[:-3].strip(), "%Y년 %m월 %d일").date()
                print(version, patchDate, date.today())
                if date.today() < patchDate:
                    return (rd[i-1])[0]

print(getLiveClientVersion())