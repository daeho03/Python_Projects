#pip install matplotlib
#pip install numpy
import pymysql
#그래프 출력 라이브러리
import matplotlib.pyplot as plt
import numpy as np
#한글 깨짐 해결용
import matplotlib.font_manager as fm
#문자열 수정용
import re

conn = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'testdb', charset='utf8')
curs = conn.cursor()

#설문 출력을 위한 변수
survey_targets = {"평균" : "men_and_women", "남성평균" : "men", "여성평균" : "women"
                    , "10대" : "teens", "20대" : "twenties", "30대" : "thirties", "40대" : "forties", "50대" : "fifties"}
survey_target_keys = list(survey_targets.keys())
survey_target_values = list(survey_targets.values())
years = [2015, 2016, 2017, 2018, 2019, 2020]
tables = ['day_play_time', 'one_play_time', 'monthly_cost', 'game_genre', 'play_percentage', 'played_a_lot', 'game_played_mostly', 'game_genre_played_mostly', 'duration_of_gameplay', 'total_played_games', 'covid19']
table_info = {'day_play_time' : "1일 플레이 타임", 'one_play_time' : "1회 플레이 타임", 'monthly_cost' : "월 게임 지출", 'game_genre' : "플레이 해본 게임 장르", 'play_percentage' : "이용비중"
            , 'played_a_lot' : "주로 플레이하는 게임 장르", 'game_played_mostly' : "주로 플레이하는 게임 수", 'game_genre_played_mostly' : "주로 플레이하는 게임 장르", 'duration_of_gameplay' : "게임 당 평균 이용기간", 'total_played_games' : "플레이하는 게임 수", 'covid19' : "코로나로 인한 플레이시간 변화"}
year_tables = {2015 : ["game_genre", "play_percentage", "day_play_time", "one_play_time", "total_played_games", "game_played_mostly", "duration_of_gameplay", "monthly_cost", "game_genre_played_mostly"]
                , 2016 : ["game_genre", "play_percentage", "day_play_time", "one_play_time", "total_played_games", "game_played_mostly", "duration_of_gameplay", "monthly_cost", "game_genre_played_mostly"]
                , 2017 : ["game_genre", "play_percentage", "day_play_time", "one_play_time", "total_played_games", "game_played_mostly", "duration_of_gameplay", "monthly_cost", "game_genre_played_mostly"]
                , 2018 : ["game_genre", "day_play_time", "one_play_time", "total_played_games", "game_played_mostly", "duration_of_gameplay", "monthly_cost", "game_genre_played_mostly"]
                , 2019 : ["game_genre", "played_a_lot" , "day_play_time", "one_play_time", "total_played_games", "game_played_mostly", "duration_of_gameplay", "monthly_cost", "game_genre_played_mostly"]
                , 2020 : ["game_genre", "played_a_lot", "day_play_time", "one_play_time", "total_played_games", "game_played_mostly", "duration_of_gameplay", "monthly_cost", "game_genre_played_mostly", "covid19"]
                }

#게임 정보 출력을 위한 변수
games = {
    "RPG" : ["위쳐3", "검은사막", "로스트아크", "리그오브레전드"]
    , "AOS" : ["리그오브레전드", "히어로즈 오브 더 스톰", "모바일 레전드"]
    , "FPS" : ["서든어택", "오버워치", "배틀그라운드"]
    , "시뮬레이션" : ["플래닛 주", "유로 트럭 시뮬레이터2", "심즈4", "이브 온라인"]
    , "스포츠" : ["FIFA온라인4"]
    }
title = ["게임", "개발사", "게임엔진", "출시연도", "플랫폼1", "플랫폼2", "플랫폼3", "플랫폼4", "플랫폼5"]

#그래프 출력을 위한 변수
font_path = r'NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path, size = 7)
x = np.arange(8)

#설문정보 출력
def Print_survey(target_year):
    targets = []
    year = 2015
    if target_year == "1":
        print("\n모든설문을 선택하셨습니다.")

        print("1. 모든대상, 2.특정대상")
        target = input("\n모든대상 또는 특정대상을 선택하세요 : ")

        if target == "1":
            print("\n모든대상을 선택하셨습니다.\n")

            while True:
                if year in years:
                    for table in tables:
                        if table in year_tables[year]:
                            sql = "select year, field, type, men_and_women, men, women, teens, twenties, thirties, forties, fifties from " + re.sub("\'", "", table) + " where year = '" + str(year) + "'"
                            curs.execute(sql)
                            survey = curs.fetchall()
                            print("\n")
                            print(survey[0][1])
                            print("-------------------------------------------" + "----------------" * 7)
                            print("\t\t\t\t\t\t", end='')
                            for tg in survey_target_keys:
                                if tg in survey_target_keys[3:]:
                                    print("{0:>12}".format(tg), end= "")
                                else:
                                    print("{0:>8}".format(tg), end= "")
                            print("\n------------------------------------------" + "----------------" * 7)
                            # 설문결과 출력
                            for line in survey:
                                count = 0
                                for v in line:
                                    if count >= 3:
                                        if count == 3:
                                            print("\n\t\t\t\t\t-> | ", end="")
                                        print("{0:>10}".format(v), end=" | ")
                                    else:
                                        if count == 2:
                                            print("{0:>8}".format(v), end=" ")
                                        else:
                                            print("{0:<8}".format(v), end=" ")
                                    count += 1
                                print("\n-------------------------------------------" + "----------------" * 7)
                            print(table_info[table])
                else:
                    print("\n잘못된 입력입니다.")
                    year = "입력창"
                print("\n- 2015, 2016, 2017, 2018, 2019, 2020 -")
                print("\t현재 페이지 :", year)
                year = input("\n페이지 입력(0 -> 초기화면) : ")
                if year == "0":
                    print("\n초기화면으로 이동\n")
                    return 0
                year = int(year)
        elif target == "2":
            print("\n특정대상을 선택하셨습니다.\n설문대상 : ", end='')
            index = 1
            for tg in survey_target_keys:
                print("{0}. {1}".format(index, tg), end=' ')
                index += 1

            survey_target = input("\n\n설문대상을 선택하세요(구분자 : ',') : ").split(',')

            index = 0
            for i in survey_target:
                survey_target[index] = survey_target_keys[int(i) - 1]
                index += 1

            #설문대상 입력 검사
            for tg in survey_target:
                if tg not in survey_target_keys:
                    print("\n잘못된 입력입니다.\n")
                    return -1
                targets.append(survey_targets[tg])
            
            #리스트로 받은 설문대상을 쿼리문에서 쓰기위해 대괄호 제외한 전체를 문자열로 변경
            targets_sql = str(targets)[1 : -1]
            targets_sql = re.sub("\'", "", targets_sql)
            while True:
                if year in years:
                    for table in tables:
                        if table in year_tables[year]:
                            sql = "select year, field, type, " + targets_sql + " from " + re.sub("\'", "", table) + " where year = '" + str(year) + "'"
                            curs.execute(sql)
                            survey = curs.fetchall()
                            print("\n")
                            print(survey[0][1])
                            print("-------------------------------------------" + "----------------" * len(survey_target))
                            print("\t\t\t\t\t\t", end='')
                            count = 0
                            for tg in survey_target:
                                if tg in survey_target_keys[3:]:
                                    print("{0:>12}".format(tg), end= "")
                                else:
                                    print("{0:>8}".format(tg), end= "")
                            print("\n------------------------------------------" + "----------------" * len(survey_target))
                            # 설문결과 출력
                            for line in survey:
                                count = 0
                                for v in line:
                                    if count >= 3:
                                        if count == 3:
                                            print("\n\t\t\t\t\t-> | ", end=" ")
                                        print("{0:>10}".format(v), end=" | ")
                                    else:
                                        if count == 2:
                                            print("{0:>8}".format(v), end=" ")
                                        else:
                                            print("{0:<8}".format(v), end=" ")
                                    count += 1
                                print("\n-------------------------------------------" + "----------------" * len(survey_target))
                            print(table_info[table])
                else:
                    print("\n잘못된 입력입니다.")
                    year = "입력창"
                print("\n- 2015, 2016, 2017, 2018, 2019, 2020 -")
                print("\t현재 페이지 :", year)
                year = int(input("\n페이지 입력(0 -> 초기화면) : "))
                if year == 0:
                    print("\n초기화면으로 이동\n")
                    return 0
        else:
            print("\n잘못된 입력입니다.\n")
    elif target_year == '2':
        print("1. 2015, 2. 2016, 3. 2017, 4. 2018, 5. 2019, 6. 2020")
        target_year = int(input("\n1 ~ 6 중 하나를 선택하세요 : "))
        target_year = str(years[target_year - 1])
        print("\n" + target_year + "년도 설문을 선택하셨습니다.\n")

        print("-----------------------------")
        print(target_year + "년도의 설문")
        print("-----------------------------")
        index = 1
        for i in year_tables[int(target_year)]:
            print("{0}. {1}".format(index, table_info[i]))
            index += 1
        print("-----------------------------")

        fields = input("\n출력할 설문을 입력하세요(구분자 : ',') : ").split(',')

        # 설문 입력 검사
        for field in fields:
            if year_tables[int(target_year)][int(field) - 1] not in year_tables[int(target_year)]:
                print("\n잘못된 입력입니다.\n")
                return -1
        
        for field in fields:
            sql = "select year, field, type, men_and_women, men, women, teens, twenties, thirties, forties, fifties from " + re.sub("\'", "", year_tables[int(target_year)][int(field) - 1]) + " where year = '" + str(target_year) + "'"
            curs.execute(sql)
            survey = curs.fetchall()
            print("\n")
            print(survey[0][1])
            print("-------------------------------------------" + "----------------" * 7)
            print("\t\t\t\t\t\t", end='')
            for tg in survey_target_keys:
                if tg in survey_target_keys[3:]:
                    print("{0:>12}".format(tg), end= "")
                else:
                    print("{0:>8}".format(tg), end= "")
            print("\n------------------------------------------" + "----------------" * 7)
            # 설문결과 출력
            for line in survey:
                count = 0
                for v in line:
                    if count >= 3:
                        if count == 3:
                            print("\n\t\t\t\t\t-> | ", end="")
                        print("{0:>10}".format(v), end=" | ")
                    else:
                        if count == 2:
                            print("{0:>8}".format(v), end=" ")
                        else:
                            print("{0:<8}".format(v), end=" ")
                    count += 1
                print("\n-------------------------------------------" + "----------------" * 7)
            print(table_info[year_tables[int(target_year)][int(field) - 1]])
            print()

# 게임정보 출력
def Print_gameInfo(genre):
    game_list = []
    if genre in years:
        sql = "select type from game_genre_played_mostly where year = " + re.sub("\'", "", str(genre))
        curs.execute(sql)
        input_genres = curs.fetchall()
        game_genres = []

        print("-----------------------------")
        index = 1
        for game in input_genres:
            print("{0}. {1}".format(index, game[0]))
            game_genres.append(game[0])
            index += 1
        print("-----------------------------")

        game_genre = int(input("\n하나의 장르를 선택하세요(0 -> 초기화면) : "))
        if game_genre >= 1 and game_genre < index:
            game_genre = game_genres[game_genre - 1]

            sql = "select men_and_women, men, women, teens, twenties, thirties, forties, fifties from game_genre_played_mostly where year = " + re.sub("\'", "", str(genre)) + " and type = '" + game_genre + "'"
            curs.execute(sql)
            info = list(curs.fetchone())

            plt.title(game_genre, fontsize = 25, fontproperties=fontprop)
            plt.xlabel('Survey targets', fontsize=18)
            plt.ylabel('Percentage', fontsize=18)
            plt.yticks(np.arange(0, 100, 5))
            plt.bar(survey_target_values, info)

            for i, v in enumerate(survey_target_values):
                plt.text(v, info[i], info[i],                # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                        fontsize = 9, 
                        color='blue',
                        horizontalalignment='center',  # horizontalalignment (left, center, right)
                        verticalalignment='bottom')    # verticalalignment (top, center, bottom)

            plt.show()
            print()
        else:
            print("\n잘못된 입력입니다.\n")
            return -1            

        if game == 0:
            print("\n초기화면으로 이동\n")
            return 0
    else:
        print("\n" + genre + " 장르를 선택하셨습니다.")

        sql = "select gameName from gameInfo where type = '" + genre + "'"
        curs.execute(sql)
        game_names = curs.fetchall()

        print("-----------------------------")
        print(genre + "장르의 게임")
        print("-----------------------------")
        index = 1
        for name in game_names:
            print("{0}. {1}".format(index, name[0]))
            index += 1
            game_list.append(name[0])
        print("-----------------------------")

        game = int(input("\n하나의 게임을 선택하세요(0 -> 초기화면) : "))
            
        if game == 0:
            print("\n초기화면으로 이동\n")
            return 0

        print()
        if game_list[game - 1] in games[genre]:
            sql = "select gameName, dev, engine, year, platform1, platform2, platform3, platform4, platform5 from gameInfo where type = '" + genre + "' and gameName = '" + game_list[game - 1] + "'"
            curs.execute(sql)
            game_info = curs.fetchone()
            
            print("-----------------------------")
            index = 0
            for line in game_info:
                if(line != ""):
                    print(title[index], end=" : ")
                    print(line)
                    index += 1
            print("-----------------------------\n")
        else:
            print("잘못된 입력입니다")