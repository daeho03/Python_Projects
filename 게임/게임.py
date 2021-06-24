import pymysql
import time

conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

seed_money = 0
login = False
played = False

def Reset():
    sqls = ["truncate table user",
            "truncate table dividend",
            "truncate table admin",
            "insert into user values('admin', '1234', '0')",
            "insert into dividend values('...', 'admin', '100000')",
            "insert into admin values('deposit', '0')",
            "insert into admin values('signup', '0')",
            "insert into admin values('game', '1')",
            "insert into admin values('play', '0')",
            "insert into admin values('...', '4')"]
    for sql in sqls:
        curs.execute(sql)
    conn.commit()

def Result():
    sql = "select arrowed from admin where section = 'game'"
    curs.execute(sql)
    if int(curs.fetchone()[0]) == 0:
        dividend = {}
        sql = "select section from admin where arrowed = 4"
        curs.execute(sql)
        answer = str(curs.fetchone()[0])
        sql = "select id from dividend where loc = '{}'".format(answer)
        curs.execute(sql)
        winners = curs.fetchall()
        if not winners:
            print("\n당첨자가 없습니다")
        else:
            for winner in winners:
                sql = "select sum(money) from dividend where loc = '{}' and id = '{}'".format(answer, winner[0])
                curs.execute(sql)
                dividend[winner[0]] = int(curs.fetchone()[0])
            sql = "select sum(money) from dividend"
            curs.execute(sql)
            d_money = int(curs.fetchone()[0]) * 0.8
            n = d_money/sum(dividend.values())
            names = list(dividend.keys())
            index = 0

            print("\n*당첨자*")
            for m in dividend.values():
                sql = "select sum(money) from dividend where id = '{}'".format(names[index])
                curs.execute(sql)
                all_m = int(curs.fetchone()[0])
                print("아이디 : {}\n\t- 전체배당금 : {}원\n\t- 당첨금 : {}원".format(names[index], all_m, int(m * n)))
                index += 1
            time.sleep(2)
    else:
        sql = "select arrowed from admin where section = 'play'"
        curs.execute(sql)
        if int(curs.fetchone()[0]) == 1:
            print("\n게임이 진행중입니다.")
        else:
            print("\n게임이 종료되어있습니다.")
        time.sleep(1)

while True:
    if login == False:
        print("\n프로그램종료 -> 1\n회원가입 -> 2\n로그인 -> 3\n")
        mode = int(input("메뉴 선택 : "))

        if mode == 1:
            print("\n-프로그램 종료-")
            break
        elif mode == 2:
            sql = "select arrowed from admin where section = 'signup'"
            curs.execute(sql)
            if int(curs.fetchone()[0]) == 1:
                print("\n-회원가입-")
                user_id = input("아이디를 입력하세요 : ")

                sql = "select count(*) from user where id = '{}'".format(user_id)
                curs.execute(sql)
                if int(curs.fetchone()[0]) != 0:
                    print("이미 있는 아이디입니다.")
                    time.sleep(1)
                    continue
                user_password = input("비밀번호를 입력하세요 : ")
                money = 100000
                if len(user_id) <= 20 or len(user_password) <= 20 or len(str(money)) <= 100:
                    sql = "insert into user values('{}', '{}', {})".format(user_id, user_password, money)
                    curs.execute(sql)
                    conn.commit()
                    print("\n회원가입이 완료되었습니다")
                    time.sleep(1)
                else:
                    print("\n다시입력하세요\n")
                    continue
            else:
                print("\n회원가입 기능 비활성화")
                time.sleep(1)

        elif mode == 3:
            print("\n-로그인-")
            user_id = input("아이디를 입력하세요 : ")
            user_password = input("비밀번호를 입력하세요 : ")
            sql = "select id, money from user where id = '{}' and password = '{}'".format(user_id, user_password)
            curs.execute(sql)
            c = curs.fetchone()
            if c != None:
                c = list(c)
                user_id = c[0]
                user_money = c[1]
                login = True
            else:
                print("\n-잘못된입력입니다-")
                continue
        else:
            print("\n-잘못된입력입니다-")
            continue
    elif login == True:
        if user_id == "admin":
            print("\nadmin계정에 접속했습니다.\n회원가입 설정 -> 1, 입금 설정 -> 2, 게임시작 -> 3, 게임종료 -> 4, 로그아웃 -> 5, 초기화-> 6")
            mode = int(input("입력하세요 : "))
            if mode == 1:
                arrow = int(input("회원가입(활성화 -> 1, 비활성화 -> 0) : "))
                if arrow == 1 or arrow == 0:
                    sql = "update admin set arrowed = '{}' where section = 'signup'".format(arrow)
                    curs.execute(sql)
                    conn.commit()
                    print("\n설정변경됨")
                    time.sleep(1)
                else:
                    print("\n잘못된 입력입니다.")
                continue
            elif mode == 2:
                arrow = int(input("입금(활성화 -> 1, 비활성화 -> 0) : "))
                if arrow == 1 or arrow == 0:
                    sql = "update admin set arrowed = '{}' where section = 'deposit'".format(arrow)
                    curs.execute(sql)
                    conn.commit()
                    print("\n설정변경됨")
                    time.sleep(1)
                else:
                    print("\n잘못된 입력입니다.")
                continue
            elif mode == 3:
                sql = "update admin set arrowed = 1 where section = 'play'"
                curs.execute(sql)
                conn.commit()
                print("\n게임이 시작되었습니다.")
                time.sleep(1)
            elif mode == 4:
                sql = "select arrowed from admin where section = 'game'"
                curs.execute(sql)
                if int(curs.fetchone()[0]) == 1:
                    answer = input("정답을 입력하세요(입력형식 -> 0:0, 0 ~ 4) : ")
                    if len(answer) == 3 and answer[1] == ":" and int(answer[0]) < 5 and int(answer[2]) < 5:
                        sqls = ["update admin set section = '{}' where arrowed = 4".format(answer),
                                "update admin set arrowed = {} where section = 'play'".format(0),
                                "update admin set arrowed = {} where section = 'game'".format(0)]
                        for sql in sqls:
                            curs.execute(sql)
                        conn.commit()
                        print("\n게임종료")
                        time.sleep(1)
                    else:
                        print("\n잘못된 입력입니다.")
                else:
                    print("\n게임이 종료되어있습니다.")
                    time.sleep(1)
                continue
            elif mode == 5:
                login = False
                print("\n로그아웃되었습니다.")
                time.sleep(1)
                continue
            elif mode == 6:
                Reset()
                print("\n초기화 완료")
                time.sleep(1)
            else:
                print("\n잘못된입력입니다")
                continue
        else:
            if played == False:
                print("\n아이디 : {}, 소지금 : {}".format(user_id, user_money))
                print("\n프로그램종료 -> 1\n로그아웃 -> 2\n게임시작 -> 3\n게임종료 및 결과확인 -> 4\n입금 -> 5\n")
                mode = int(input("메뉴 선택 : "))
                if mode == 1:
                    print("\n-프로그램 종료-")
                    break
                elif mode == 2:
                    print("\n-로그아웃되었습니다-")
                    time.sleep(1)
                    login = False
                    continue
                elif mode == 3:
                    played = True
                elif mode == 4:
                    login = False
                    Result()
                elif mode == 5:
                    sql = "select arrowed from admin where section = 'deposit'"
                    curs.execute(sql)
                    if int(curs.fetchone()[0]) == 1:
                        print("\n소지금 :", user_money)
                        i_money = int(input("입금하실 금액을 입력하세요(숫자만 입력가능, 0 입력시 취소) : "))
                        user_money = user_money + i_money
                        sql = "update user set money = {} where id = '{}'".format(user_money, user_id)
                        curs.execute(sql)
                        conn.commit()
                        print("입금이 완료되었습니다.\n잔액 :", user_money)
                    else:
                        print("\n입금기능 비활성화")
                        time.sleep(1)
                else:
                    print("\n-잘못된입력입니다-")
                    continue
            
            if played == True:
                print("\n게임종료 -> X, 배당금 -> ALL, 소지금 -> M, 배당률 출력 -> P\n0 ~ 4점 사이만 입력가능합니다")

                ch = input("\n(입력형식 -> 0:0) : ")

                if ch.lower() == "x":
                    print("\n-게임종료-")
                    played = False
                    continue
                elif ch.lower() == "all":
                    sql = "select sum(money) from dividend"
                    curs.execute(sql)
                    c = curs.fetchone()
                    seed_money = int(c[0])
                    print("\n총 배당금 :", seed_money * 0.8, "(회사 : {})".format(seed_money * 0.2))
                    continue
                elif ch.lower() == "m":
                    print("\n소지금 : {}".format(user_money))
                    continue
                elif ch.lower() == "p":
                    print("\n{}".format("-" * 41))
                    for i in range(5):
                        if i == 0:
                            print("|\| {}\t".format(i), end="")
                        else:
                            print("|   {}\t".format(i), end="")
                    print("|\n{}".format("-" * 41))
                    for i in range(0, 5):
                        if i != 0:
                            print()
                        print("|{}| ".format(i), end="")
                        for j in range(0, 5):
                            sql = "select count(*) from dividend where loc = '{}:{}'".format(i, j)
                            curs.execute(sql)
                            count = int(curs.fetchone()[0])
                            if count != 0:
                                sql = "select sum(money) from dividend where loc = '{}:{}'".format(i, j)
                                curs.execute(sql)
                                money = int(curs.fetchone()[0])
                                sql = "select sum(money) from dividend"
                                curs.execute(sql)
                                c = curs.fetchone()
                                seed_money = int(c[0]) * 0.8
                                rate = seed_money/money
                                rate = str(rate)
                                rate = float(rate[:rate.find(".") + 2])
                                if len(str(rate)) == 4 and j == 0:
                                    print(rate, end="| ")
                                else:
                                    print(rate, end="")
                                    print("\t| ", end="")
                            else:
                                print("X", end="")
                                print("\t| ", end="")
                    print("\n{}".format("-" * 41))
                    continue
                else:
                    money = int(input("금액 입력 : "))
                    
                    sql = "select arrowed from admin where section = 'play'"
                    curs.execute(sql)
                    c = int(curs.fetchone()[0])

                    if c == 0:
                        print("\n게임이 종료 되어있습니다")
                        played = False
                        time.sleep(1)
                        continue
                    elif user_money < money:
                        print("\n소지금이 부족합니다")
                    elif money >= 10000 and money <= 100000 and money <= user_money and len(ch) == 3 and ch[1] == ":" and int(ch[0]) < 5 and int(ch[2]) < 5:
                        user_money -= money
                        sqls = ["insert into dividend values('{}', '{}', {})".format(ch, user_id, money),
                                "update user set money = {} where id = '{}'".format(user_money, user_id)]
                        for sql in sqls:
                            curs.execute(sql)
                        conn.commit()
                        print("\n배팅완료")
                        time.sleep(1)
                    else:
                        print("\n다시입력하세요")
                        continue