import module

genres = ["RPG", "AOS", "FPS", "시뮬레이션", "스포츠"]
years = [2015, 2016, 2017, 2018, 2019, 2020]

while True:
    print("---------------------------------")
    print("1을 입력하시면 설문 페이지로 이동\n2를 입력하시면 게임 페이지로 이동")
    print("---------------------------------")
    section = input("입력(0 -> 종료) : ")
    if section.lower() == '0':
        print("\n프로그램 종료\n")
        break

    if section == '1':
        print("\n설문을 선택하셨습니다.")
        print("1. 모든설문,2. 2015 ~ 2020년도의 설문")
        
        year = input("\n선택하세요 : ")

        if year in ['1', '2']:
            module.Print_survey(year)
        else:
            print("\n잘못된 입력입니다.\n")
    elif section == '2':
        print("\n게임을 선택하셨습니다.")
        print("1. 게임정보 보기, 2. 장르별 선호도 보기")
        game = int(input("\n선택하세요 : "))

        if game == 1:
            print("1. RPG, 2. AOS, 3. FPS, 4. 시뮬레이션, 5. 스포츠")

            genre_index = int(input("\n하나의 장르를 선택하세요 : "))

            if genres[genre_index - 1] in genres:
                module.Print_gameInfo(genres[genre_index - 1])
            else:
                print("\n잘못된 입력입니다.\n")
        elif game == 2:
            print("1. 2015, 2. 2016, 3. 2017, 4. 2018, 5. 2019, 6. 2020")
            year = int(input("\n1 ~ 6 중 하나를 선택하세요 : "))
            year = years[year - 1]
            if year in years:
                print("\n" + str(year) + "년도를 선택하셨습니다.")
                module.Print_gameInfo(year)
            else:
                print("\n잘못된 입력입니다.\n")
    else:
        print("\n잘못된 입력입니다.\n")