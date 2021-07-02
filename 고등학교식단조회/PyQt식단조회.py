from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import requests
import re
import datetime
import pymysql
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, QGridLayout, QLabel, QLineEdit, QPlainTextEdit)

#경고문 출력x
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#DB연결
conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

#한글, 숫자
hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
non_decimal = re.compile(r'[^\d.]+')

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('학교'), 0, 0)
        grid.addWidget(QLabel('날짜'), 1, 0)
        grid.addWidget(QLabel('조회'), 2, 0)
        grid.addWidget(QLabel('결과'), 3, 0)

        self.school_name = QLineEdit("")
        self.date = QLineEdit("20210101")
        self.result = QPlainTextEdit("")
        self.search = QPushButton("식단조회")
        self.search.clicked.connect(self.Search)

        grid.addWidget(self.school_name, 0, 1)
        grid.addWidget(self.date, 1, 1)
        grid.addWidget(self.search, 2, 1)
        grid.addWidget(self.result, 3, 1)

        self.setWindowTitle('식단조회')
        self.setGeometry(400, 400, 300, 300)
        self.show()

    def Search(self):
        c = True

        date = self.date.text()

        #날짜 검사
        if int(date[0:4]) >= 2000 and int(date[4:6]) <= 12 and int(date[-2:]) <= 31 and len(date) == 8:
            #날짜가 정상적으로 들어왔으면 요일 받아오기
            day = datetime.date(int(date[0:4]),int(date[4:6]),int(date[-2:])).weekday()
            day += 3
        else:
            self.result.setPlainText("잘못된 입력입니다")
            c = False

        if c:
            name = self.school_name.text()

            #공백제거
            name = name.replace(" ", "")

            if name == "":
                self.result.setPlainText("잘못된 입력입니다")
                c = False
            if c:
                sql = "select s.code, s.name, s.loc, u.url from school s join url u on s.loc = u.loc where name like '{0}%'".format(name)
                curs.execute(sql)
                sc = curs.fetchone()

                #학교정보가 검색이 됐는지 검사
                if sc != None:
                    sc = list(sc)
                    
                    url = 'https://{0}/sts_sci_md01_001.do?schMmealScCode=2&schulCode={1}&schulCrseScCode=4&schulKndScCode=04&schYmd={2}'.format(sc[3], sc[0], date)

                    #사이트에 인증서가 없어도 접속가능하게 설정
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

                        result = ""
                        #출력
                        result += "=====================================\n"
                        result += "{} : {}\n  *{}식단*".format(sc[2], sc[1], date)
                        if(menu[0] != ""):
                            result += "\n칼로리 : {0}kcal\n\n".format(kcal)
                            for i in menu:
                                if i != "":
                                    result += " - {0}\n".format(i)
                        else:
                            result += "\n    식단 없음"
                        result += "\n====================================="
                        self.result.setPlainText(result)
                else:
                    self.result.setPlainText("학교정보 없음")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())