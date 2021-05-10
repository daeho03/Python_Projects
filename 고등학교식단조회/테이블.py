#pip install pymysql
import pymysql
import csv

conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

file = open('학교정보.csv', 'r', encoding = 'cp949')
school = csv.reader(file)

sql = "create table url(loc varchar(2), url varchar(13))default character set utf8 collate utf8_general_ci;"
curs.execute(sql)

sql = "create table school(name varchar(30), loc varchar(2),code varchar(10))default character set utf8 collate utf8_general_ci;"
curs.execute(sql)

for line in school:
    sql = "insert into school values(%s, %s, %s)"
    curs.execute(sql, line)

file = open('링크.csv', 'r', encoding = 'cp949')
url = csv.reader(file)

for line in url:
    sql = "insert into url values(%s, %s)"
    curs.execute(sql, line)

conn.commit()
conn.close()
