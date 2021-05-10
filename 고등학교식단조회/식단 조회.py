#pip install BeautifulSoup4
#pip install requests
#pip install datetime
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import requests
import re
import datetime
import pymysql

#경고문 출력x
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#DB연결
conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
non_decimal = re.compile(r'[^\d.]+')

while True:
    #날짜 입력
    date = input("날짜입력(YYYYMMDD, x -> exit) : ")

    if date == "x":
        print("\n프로그램 종료\n")
        break

    #날짜 검사
    if int(date[0:4]) >= 2000 and int(date[4:6]) <= 12 and int(date[-2:]) <= 31 and len(date) == 8:
        #날짜가 정상적으로 들어왔으면 요일 받아오기
        day = datetime.date(int(date[0:4]),int(date[4:6]),int(date[-2:])).weekday()
        day += 3
    else:
        print("\n잘못된 입력입니다\n")
        continue

    name = input('학교이름 입력 : ')
    #공백제거
    name = name.replace(" ", "")
    if name == "":
        print("\n잘못된 입력입니다\n")
        continue

    sql = "select s.code, s.name, s.loc, u.url from school s join url u on s.loc = u.loc where name like '{0}%'".format(name)
    curs.execute(sql)
    sc = curs.fetchone()

    #학교정보가 검색이 됐는지 검사
    if sc != None:
        sc = list(sc)
        
        url = 'https://{0}/sts_sci_md01_001.do?schMmealScCode=2&schulCode={1}&schulCrseScCode=4&schulKndScCode=04&schYmd={2}'.format(sc[3], sc[0], date)

        #사이트에 인증서가 없어도 접속o
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            menu = str(soup.select('#contents > div:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child({0})'.format(day)))
            menu = menu.split('<br/>')
            kcal = str(soup.select("#contents > div:nth-child(2) > table > tbody > tr:nth-child(51) > td:nth-child({0})".format(day)))

            # 한글 제외 모든 문자 제거
            index = 0
            for i in menu:
                menu[index] = hangul.sub('', menu[index])
                menu[index] = menu[index].replace(" ", "")
                index += 1
            
            #숫자 제외 모든 문자 제거
            kcal = re.sub('<.+?>', '', kcal, 0).strip()
            kcal = non_decimal.sub('', kcal)

            #출력
            print("\n=================================================\n")
            print(sc[2], ":", sc[1], "\n\n  *{0}식단*".format(date))
            if(menu[0] != ""):
                print("칼로리 : {0}kcal\n".format(kcal))
                for i in menu:
                    if i != "":
                        print(" - {0}".format(i))
            else:
                print("\n    식단 없음")
            print("\n=================================================\n")
    else:
        print("\n학교정보 없음\n")