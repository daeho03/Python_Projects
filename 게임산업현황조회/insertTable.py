import pymysql
import csv

conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

# 연도별 게임 설문 데이터 테이블에 데이터 삽입
file = open('mainDB.csv', 'r', encoding = 'cp949')
main_db = csv.reader(file)

index = 0
table_name = {'1일기준이용시간' : 'day_play_time', '1회기준이용시간' : 'one_play_time', '월평균비용' : 'monthly_cost', '이용분야' : 'game_genre', '이용비중' : 'play_percentage', '자주이용한분야' : 'played_a_lot', '주이용개수' : 'game_played_mostly', '주이용장르' : 'game_genre_played_mostly', '지속이용기간' : 'duration_of_gameplay', '총이용개수' : 'total_played_games', '코로나' : 'covid19'}
table_index = 0

for line in main_db:
    sql = "INSERT INTO " + table_name[line[1]] + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    curs.execute(sql, line)

#대표게임 출력을 위한 테이블에 데이터 삽입
file = open('gameDB.csv', 'r', encoding = 'cp949')
gameInfo_db = csv.reader(file)

sql = "INSERT INTO gameInfo VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

for line in gameInfo_db:
    curs.execute(sql, line)

conn.commit()
conn.close()