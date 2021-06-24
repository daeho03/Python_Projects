import pymysql

conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

sqls = ['''
        create table user(
        id varchar(20),
        password varchar(20),
        money int(100));
        ''',
        '''
        create table dividend(
        loc varchar(3),
        id varchar(20),
        money int(100));
        ''',
        '''
        create table admin(
        section varchar(10),
        arrowed int(1));
        ''',
        "insert into user values('admin', '1234', '0');",
        "insert into dividend values('...', 'admin', '100000');",
        "insert into admin values('deposit', '0');",
        "insert into admin values('signup', '0');",
        "insert into admin values('game', '1');",
        "insert into admin values('play', '0');",
        "insert into admin values('...', 4);"]

for sql in sqls:
    curs.execute(sql)
conn.commit()