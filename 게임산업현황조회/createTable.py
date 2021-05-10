#pip install pymysql
import pymysql

conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

imp = '''year int(4),
field varchar(14),
type varchar(11),
men_and_women float(4, 1),
men float(4, 1),
women float(4, 1),
teens float(4, 1),
twenties float(4, 1),
thirties float(4, 1),
forties float(4, 1),
fifties float(4, 1)'''

# 설문 테이블 생성
sql = "create table game_genre(" + imp + ");"
curs.execute(sql)
sql = "create table played_a_lot(" + imp + ");"
curs.execute(sql)
sql = "create table play_percentage(" + imp + ");"
curs.execute(sql)
sql = "create table day_play_time(" + imp + ");"
curs.execute(sql)
sql = "create table total_played_games(" + imp + ");"
curs.execute(sql)
sql = "create table game_played_mostly(" + imp + ");"
curs.execute(sql)
sql = "create table duration_of_gameplay(" + imp + ");"
curs.execute(sql)
sql = "create table monthly_cost(" + imp + ");"
curs.execute(sql)
sql = "create table game_genre_played_mostly(" + imp + ");"
curs.execute(sql)
sql = "create table covid19(" + imp + ");"
curs.execute(sql)
sql = "create table one_play_time(" + imp + ");"
curs.execute(sql)

# 대표게임 출력을 위한 테이블
sql = '''create table gameInfo(
game varchar(4),
type varchar(7),
gameName varchar(14),
dev varchar(14),
engine varchar(14),
year int(4),
platform1 varchar(11),
platform2 varchar(11),
platform3 varchar(11),
platform4 varchar(11),
platform5 varchar(11)
);
'''
curs.execute(sql)


conn.commit()
conn.close()