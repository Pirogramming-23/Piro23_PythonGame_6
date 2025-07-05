

def subway_game(self):
        Subway_Data = {
            "1호선": ["소요산", "동두천", "의정부", "회기", "청량리", "시청", "서울역", "용산", "구로", "인천", "신창", "광명", "서동탄"],
            "2호선": ["시청", "을지로입구", "왕십리", "성수", "잠실", "삼성", "강남", "사당", "신도림", "홍대입구", "신촌", "까치산"],
            "3호선": ["대화", "정발산", "백석", "삼송", "연신내", "불광", "경복궁", "충무로", "압구정", "고속터미널", "수서", "오금"],
            "4호선": ["진접", "별내별가람", "당고개", "노원", "창동", "혜화", "명동", "서울역", "사당", "금정", "안산", "오이도", "미아"],
            "5호선": ["방화", "김포공항", "까치산", "목동", "여의도", "공덕", "왕십리", "군자", "천호", "하남검단산", "마천", "마포"],
            "6호선": ["응암", "불광", "디지털미디어시티", "합정", "공덕", "삼각지", "이태원", "약수", "동묘앞", "석계", "화랑대", "신내"],
            "7호선": ["장암", "도봉산", "노원", "태릉입구", "건대입구", "강남구청", "고속터미널", "대림", "온수", "부평구청", "석남"],
            "8호선": ["암사", "천호", "잠실", "석촌", "가락시장", "복정", "모란", "문정" , "남위례", "남한산성 입구", "수진", "장지"],
            "9호선": ["개화", "김포공항", "가양", "당산", "여의도", "노량진", "동작", "고속터미널", "신논현", "종합운동장", "중앙보훈병원"],
            "수인분당선": ["청량리", "왕십리", "강남구청", "선릉", "수서", "모란", "정자", "수원", "오이도", "인천", "선정릉"],
            "신분당선": ["신사", "논현", "신논현", "강남", "양재", "판교", "정자", "광교중앙", "광교", "동천", "수지구청"]
        }
        valid_lines = list(Subway_Data.keys())

        print("\n🚇 지하철~ 지하철~ 지하철 지하철 🚉 몇호선!? 몇호선!? 몇호선?! 몇호선?!")

        # 시작 플레이어를 랜덤으로 선택
        starting_player = random.choice(self.participants)
        starting_player_name = starting_player['name']
        start_index = -1
        for i, p in enumerate(self.participants):
            if p['name'] == starting_player_name:
                start_index = i
                break
        
        print(f"시작 플레이어는 {starting_player_name}님 입니다!")

        if starting_player['name'] == self.player_name: # 사용자가 시작
            onemorechance = False
            while True:
                line_in = input(f"[{starting_player_name}님] 어떤 호선을 선택하시겠어요?(ex: 1호선) : ").strip()
                if line_in in valid_lines:
                    chosen_line = line_in
                    break
                else:
                    if onemorechance:
                        print("\n💥 두 번 연속으로 잘못된 노선을 선택했습니다! 💥")
                        return starting_player_name
                    else:
                        print("살리고 살리고~! 유효한 노선을 선택해주세요(1호선-9호선, 신분당선, 수인분당선)")
                        onemorechance = True
        else: # 컴퓨터가 시작
            chosen_line = random.choice(valid_lines)
            print(f"{starting_player_name}: {chosen_line}!")

        print(f"\n선택된 노선: {chosen_line}의 역 이름을 순서대로 말해주세요!")
        used_stations = []
        current_turn_index = start_index

        while True:
            current_player = self.participants[current_turn_index]
            is_correct = False

            if current_player['name'] == self.player_name: # 사용자 턴 - 지하철 나열
                answer = input(f"\n[{current_player['name']}님 턴] {current_player['name']}: ").strip()
                if answer in used_stations:
                    print(f"❌ '{answer}'은/는 이미 나온 역입니다!")
                elif answer in Subway_Data[chosen_line]:
                    used_stations.append(answer)
                    is_correct = True
                else:
                    print(f"❌ '{answer}'은/는 {chosen_line}에 없는 역입니다!")
            else: # 컴퓨터 턴 - 지하철 나열
                print(f"\n[{current_player['name']}님 턴...]")
                time.sleep(1)
                if random.random() < 0.85: # 85% 확률로 정답 맞추기
                    available_stations = [s for s in Subway_Data[chosen_line] if s not in used_stations]
                    if available_stations:
                        com_ans = random.choice(available_stations)
                        print(f"{current_player['name']}: {com_ans}")
                        used_stations.append(com_ans)
                        is_correct = True
                    else:
                        print(f"{current_player['name']}: ...더 이상 역이 생각이 안 나..!")
                else:
                    print(f"{current_player['name']}: 으음...모르겠어..!")
            
            if not is_correct:
                return current_player['name'] 

            current_turn_index = (current_turn_index + 1) % len(self.participants)
