import random
import time
import numpy as np ### 요거 추가했어!
import pandas as pd
import re

class alcohol_game:
    def __init__(self):
        # 플레이어 이름
        self.player_name = ""
        self.alcohol_limit = 0

    
    # 인트로 함수 너무 빨리 출력된다고 생각들면 추후 sleep 시간 조정가능

        self.game_list = {"아파트":self.apartment_game, "끝말잇기":self.play_end_word_game, "369게임":self.game_369, "노선게임":self.subway_game}
        self.player_names = []
        self.participants = []
        self.word_list = self.extract_nouns_from_csv("kr_korean.csv")
        self.rng = np.random.default_rng() ### 요거 추가했어 !!!

    def intro(self):
        intro = r"""
            .　∧∧　■
            　(＾ω＾)／　술 게임을 시작할게요^^~
            　＜　　/
            　　∪∪
----------------------------------------------------------------------------------------------
누가 술을 마셔? 너가 술을 마셔~
----------------------------------------------------------------------------------------------

        """
        for line in intro.splitlines():
            print(line)
            time.sleep(0.3)

            
    # 참여자 추가
    def add_participant(self, name, limit):
        self.participants.append({'name':name, 'limit':limit, 'drunk':0})
        self.player_names.append(name)
            
    # 주량 선택
    def select_alcohol_limit(self):
        select = [2, 4, 6, 8, 10]
        alcohol_menu = (
            "-------------🍺소주 얼만큼 드세요(수줍)---{\\__/}------\n"
            "-------------1. 반병 (2잔)🍻-------------(̷ ̷´̷ ̷^̷ ̷`̷)̷◞♡---\n"
            "-------------2. 반병에서 한병 (4잔)🍹------|  ⫘ |------\n"
            "-------------3. 한병에서 한병반 (6잔)🍸------------------\n"
            "-------------4. 한병반에서 두병 (8잔)🍷------------------\n"
            "-------------5. 두병 이상 (10잔)🍾----------------------\n"
        )
        
        # 여기서 목숨 선택
        while True:
            print(alcohol_menu)
            choice = input("당신의 치사량을 선택하세요(1~5): ").strip()
            if choice in ('1','2','3','4','5'):
                self.alcohol_limit = select[int(choice)-1]
                print(f"> 설정된 주량: {self.alcohol_limit}잔\n")
                break
            else:
                print("잘못 선택했습니다. 다시 골라주세요\n")
    
    # 참여자 추가
    def invite_participants(self):
        participants = ["은서","하연","연서","예진", "헌도"]
        
        while True:
            try:
                n = int(input("초대할 사람 수(최대 3명)").strip())
                if 0 <= n <= 3:
                    break
            except ValueError:
                pass
            print("3명까지만 불러주세요 친구들이 3명만 온데요")
        chosen_participants = random.sample(participants, n)
        
        # 친구들의 목숨
        for part in chosen_participants:
            limit_drink = random.choice([2, 4, 6, 8, 10])
            self.add_participant(part, limit_drink)

        print("\n 현재 상태: ")

        for i in self.participants:
            remain_limit = i['limit'] - i['drunk']
            print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")

        print("\n참가자 리스트:")
        print(", ".join(self.player_names), "\n")
        
    # 게임이 돌아가는 로직 구현
    def play(self):
        print(f"{self.player_name}님의 주량은 ({self.alcohol_limit}잔) 입니다.")
        while True:
            # 게임 리스트
            print("\n------------게임을 골라주세요------------")
            for idx, game_name in enumerate(self.game_list.keys(), start=1):
                print(f"{idx}. {game_name}")
            print("------------게임을 골라주세요------------")

            select = input("게임을 골라주세요: ").strip()
            try:
                choice = int(select) - 1
                selected_game = list(self.game_list.keys())[choice]
            except (ValueError, IndexError):
                print("숫자를 입력해주세요. 잘못 입력했습니다.")
                continue

            print(f"\n[{selected_game}] 게임을 시작!\n")
            loser = self.game_list[selected_game]()

            # 예외처리: 아무도 안지면 다시
            if not loser:
                continue
            
            # 진 사람 색출
            participant = None
            for p in self.participants:
                if p['name'] == loser:
                    participant = p
                    break
            if not participant:
                continue

            if participant['drunk'] >= participant['limit']:
                print(f"\n{loser}님이 치사량을 넘겼습니다")
                print(fr"""
                    {loser}님 술찌시네요~~ 후후
                    ￣￣￣￣￣ヽ___ノ￣￣￣￣￣￣￣￣￣
                            Ｏ
                             o
                            ,. ─冖'⌒'─､⌒ ⌒ 〉
                           ノ       ＼  ⌒ ─､─､〉〉
                           / ,r‐へへく⌒'￢､  ヽ〉
                          {{ノ へ._、 ,,／~`  〉 ｝
                         ／プ￣￣`y'¨Y´￣￣ヽ─}}j=く
                        ノ /レ'>ー{{___ｭ`ーー'  ﾘ,ｲ}}
                       / _勺 ｲ;；∵r===､､∴'∵;  シ 
                      ,/ └'ノ ＼  ご`    ノ{{ー—､__
                      人＿_/ー┬ー个-､＿＿,,.. ‐´ 〃`ァーｧー＼
                    . /  |／ |::::|､      〃 /:::/   ヽ
                    /    |  |::::|＼､_________／ /:::/〃    |
                """)
                return 

            # 컴퓨터가 질 시에 램덤으로 게임 고름
            if loser != self.player_name:
                print(f"\n{loser}이(가) 좋아하는 랜덤 게임!\n")
                time.sleep(1)
                next_game = random.choice(list(self.game_list.keys()))
                print(f"{loser}: [{next_game}] 게임!\n")
                time.sleep(1)

                
                nested_loser = self.game_list[next_game]()
                if nested_loser:
                    p2 = next((p for p in self.participants if p['name'] == nested_loser), None)
                    if p2 and p2['drunk'] >= p2['limit']:
                        print(f"\n{nested_loser}님이 치사량을 넘겼습니다")
                        print(fr"""
                                {loser}님 술찌시네요~~ 후후
                                ￣￣￣￣￣ヽ___ノ￣￣￣￣￣￣￣￣￣
                                        Ｏ
                                         o
                                        ,. ─冖'⌒'─､⌒ ⌒ 〉
                                       ノ       ＼  ⌒ ─､─､〉〉
                                       / ,r‐へへく⌒'￢､  ヽ〉
                                      {{ノ へ._、 ,,／~`  〉 ｝
                                     ／プ￣￣`y'¨Y´￣￣ヽ─}}j=く
                                    ノ /レ'>ー{{___ｭ`ーー'  ﾘ,ｲ}}
                                   / _勺 ｲ;；∵r===､､∴'∵;  シ 
                                  ,/ └'ノ ＼  ご`    ノ{{ー—､__
                                  人＿_/ー┬ー个-､＿＿,,.. ‐´ 〃`ァーｧー＼
                                . /  |／ |::::|､      〃 /:::/   ヽ
                                /    |  |::::|＼､_________／ /:::/〃    |
                        """)
                        return
                continue
            
            # 내가 질 시에 게임 고름
            while True:
                yn = input("다음 게임 계속 하실까요?(y/n): ").strip().lower()
                if yn == 'y':
                    break
                if yn == 'n':
                    print("\n게임 종료!")
                    return
                print("잘못 입력하셨어요~ 'y'나 'n'만 눌러주세요")

            
        
    # 게임 리스트 함수
    def show_game_list(self):
        print("\n 게임 리스트")
        if not self.game_list:
            print("게임이 없는뎁쇼?!?!?")
        else:
            for i, game in enumerate(self.game_list, start=1):
                print(f"{i}. {game}\n")

    # 주량이 0이 될시 딕셔너리에 있는 사람들 out 그리고 게임 종료
    
    
    # 여기서부터 게임 파트###############################

    # ################# 아파트 게임

    def apartment_game(self):
        print("\n 아파트~~!, 아파트~~!, 아파트~~!, uh, uh-huh, uh-huh [...대충 부르노 마스 보컬]")
        
        # 참가자는 손이 2개이다
        hands = [i['name'] for i in self.participants]
        for i in self.participants:
            hands += [i['name'], i['name']]
        total_hands = len(hands)
        print(f"총 손 개수 : {total_hands}개 ({len(self.participants)}명 x 2손)\n")
        
        while True:
            try:
                floor = int(input("몇 층에 사세요?(20층 이상 입력): ").strip())
                if floor < 20:
                    print("아파트가 신축이라 20층 이상 입력해야겠네요.")
                    continue
                break
            except ValueError:
                print("숫자만 입력해주세요")
                
        for current_floor in range(1, floor+1):
            idx = (current_floor - 1) % total_hands
            current_name = hands[idx]
            print(f"{current_name}님이 {current_floor}층 한층씩 올라갑니다~~")
            time.sleep(0.2)
        
        idx = (floor - 1) % total_hands
        loser = hands[idx]
        
        for i in self.participants:
            if i['name'] == loser:
                i['drunk'] += 1
                print(f"\n {loser}님이 {floor}층에서 탈락!!!")
                
                print("\n 현재 상태: ")
                for i in self.participants:
                    remain_limit = i['limit'] - i['drunk']
                    print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                return loser

    # ###############################
    
    

    # ################### 끝말잇기
    def is_clean_korean(self, word):
        return bool(re.fullmatch(r'[가-힣]{2,}', str(word)))

    def extract_nouns_from_csv(self, path):
        try:
            df = pd.read_csv(path, encoding='utf-8')
            noun_df = df[df['어미'].str.contains('명사', na=False)]
            clean_nouns = noun_df['-가'].dropna().drop_duplicates()
            return [word for word in clean_nouns if self.is_clean_korean(word)]
        except Exception as e:
            print(f"사전 로딩 오류: {e}")
            return []

    def get_computer_word(self, last_char, used_words):
        candidates = [word for word in self.word_list if word.startswith(last_char) and word not in used_words]
        if candidates:
            return random.choice(candidates)  # 랜덤하게 선택
        return None

    def play_end_word_game(self):
        used_words = []
        last_char = None

        # 컴퓨터 대신 플레이어로 변형
        players = [self.player_name] + [i['name'] for i in self.participants if i['name'] != self.player_name]
        turn = 0
        
        print("끝말잇기를 시작합니다. '끝'을 입력하면 종료됩니다.")
        print("2글자 이상 순수 한글 단어만 사용할 수 있습니다.")

        
        while True:
            # leacy code
            # user_word = input("당신의 단어: ").strip()
            current = players[turn % len(players)]
            
            if current == self.player_name:
                word = input(f"{current}의 단어: ").strip()
                
                if word == "끝":
                    print("게임을 종료합니다.")
                    for i in self.participants:
                        if i['name'] == current:
                            i['drunk'] += 1
                            break
                    print("\n 현재 상태:")
                    for i in self.participants:
                        remain_limit = i['limit'] - i['drunk']
                        print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                    return current
                
                if len(word) < 2:
                    print("2글자 이상 단어만 입력 가능합니다.")
                    continue
                
                if word in used_words:
                    print(f"이미 사용한 단어입니다. {current}님이 졌습니다.")
                    for i in self.participants:
                        if i['name'] == current:
                            i['drunk'] += 1
                            break
                    print("\n 현재 상태:")
                    for i in self.participants:
                        remain_limit = i['limit'] - i['drunk']
                        print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                    return current
                
                if word not in self.word_list:
                    print("사전에 없는 단어입니다. 다시 입력하세요.")
                    for i in self.participants:
                        if i['name'] == current:
                            i['drunk'] += 1
                            break
                    print("\n 현재 상태:")
                    for i in self.participants:
                        remain_limit = i['limit'] - i['drunk']
                        print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                    return current
                
                if last_char and not word.startswith(last_char):
                    print(f"'{last_char}'(으)로 시작하는 단어를 입력해야 합니다.")
                    
                    for i in self.participants:
                        if i['name'] == current:
                            i['drunk'] += 1
                            break
                    print("\n 현재 상태:")
                    for i in self.participants:
                        remain_limit = i['limit'] - i['drunk']
                        print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                    return current
                
            else:
                # 다른 참가자들의 차례(leacy_code 참고)
                comp_word = self.get_computer_word(last_char, used_words)
                if comp_word:
                    print(f"{current}: {comp_word}")
                    word = comp_word
                    
                else:
                    print(f"{current}이(가) 단어를 찾지 못했습니다. {current}님이 졌습니다!")
                    for i in self.participants:
                        if i['name'] == current:
                            i['drunk'] += 1
                            break
                    print("\n 현재 상태:")
                    for i in self.participants:
                        remain_limit = i['limit'] - i['drunk']
                        print(f" - {i['name']}: 마신 {i['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                    return current
                
            used_words.append(word)
            last_char = word[-1]
            turn += 1
            # ########## leacy code
            # comp_word = self.get_computer_word(last_char, used_words)
            # if comp_word:
            #     print(f"컴퓨터: {comp_word}")
            #     used_words.append(comp_word)
            #     last_char = comp_word[-1]
            # else:
            #     print("컴퓨터가 단어를 찾지 못했습니다. 당신이 이겼습니다.")
            #     break
            # ########## leacy code
            
    # ###########################369게임
    
        # 369 게임 함수
    def game_369(self):
        print("🚨 369 게임을 시작합니다!🚨")
        print("📢 규칙: 3, 6, 9가 들어간 숫자는 짝👏을 외쳐주세요!")
        print("""
           　 ∧＿＿∧ ＿∧                                
           (（( ・ω・)三ω・)) 369 369~                      
          　　(_っっ= _っっ゜　369 369~                    
          　　 ヽ　　ノ                                 
          　　　( /￣∪                             
        """)

        current_num = 1
        #플레이러 랜덤 지정
        turn = self.rng.integers(0, len(self.participants))
        mistake_count = 0

        while True:
            player = self.participants[turn % len(self.participants)]
            name = player['name']

            count_369 = sum(1 for d in str(current_num) if d in "369")
            if count_369 == 0:
                expected = str(current_num)
            else:
                expected = "짝" * count_369
            
            #self.player_name일 때는 직접 정답 입력하고 그 외에는 랜덤으로 생성
            if name == self.player_name:
                answer = input(f">> {name}의 차례: ").strip()
            else:
                drunk = player['drunk'] # 지금까지 마신 잔 수
                limit = player['limit'] # 참가자의 전체 주량
                # 얼마나 취했는지를 비율로 표현
                if limit > 0:
                    drunk_ratio = drunk / limit
                else:
                    drunk_ratio = 0
                base_accuracy = 0.9 # 기본 90%의 정답률 
                adjusted_accuracy = base_accuracy - (drunk_ratio * 0.5) #취한 정도에 따라 정확도 깎음
                is_correct = random.random() < max(0.3, adjusted_accuracy) #아무리 취해도 30% 확률로는 맞출 수 있게 함

                if is_correct:
                    answer = expected
                else:
                    if expected == "짝":
                        answer = str(current_num)
                    else:
                        answer = "짝"
                print(f">> {name}의 차례: {answer}")
                time.sleep(1)
            if answer != expected:
                mistake_count += 1

                if mistake_count == 1:
                    print(f"❌ {name} 틀렸습니다! 😅 살리고~ 살리고~ 한 번은 봐줄게요!")
                    time.sleep(1)
                else: 
                    player['drunk'] += 1
                    print(f"❌ {name} 땡! 정답은 '{expected}'")
                    time.sleep(1)
                    print("""
                    ┏┯┯┯┯┯┓
                    ┃││∧∧│┃살려줘!!
                    ┃│(≧Д≦)┃
                    ┃││ф ф│┃
                    ┗┷┷┷┷┷┛
                            """)
                    time.sleep(1)
                    print(f"🚨 전체 두 번째 실수 발생! 더 이상 못 살려~ 게임 종료! 🚨")
                    time.sleep(1)
                    # 전체 상태 출력
                    print("\n 현재 상태:")
                    for p in self.participants:
                        remain_limit = p['limit'] - p['drunk']
                        print(f" - {p['name']}: 마신 {p['drunk']}잔🍺, 남은 {remain_limit}잔🍺")

                    # 패자 이름 반환
                    return name
            else:
                print(f"✅ {name} 정답!\n")

            current_num += 1
            turn += 1
    # ############################
    
    # ######################### 전철 게임 
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
        print("🚇 지하철~ 지하철~ 몇호선?! 몇호선?! 🚇")

        # 시작 플레이어 랜덤 선택
        starting_player = random.choice(self.participants)
        starting_player_name = starting_player['name']
        start_index = self.participants.index(starting_player)
        
        print(f"시작은 {starting_player_name}님부터!")

        # 호선 선택
        chosen_line = ""
        if starting_player_name == self.player_name:
            onemorechance =False
            while True:
                line_in = input(f"[{self.player_name}님] 호선을 선택하세요 (ex: 1호선): ").strip()
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
        else:
            print(f"[{starting_player_name}님]이(가) 노선을 선택합니다...")
            time.sleep(1)
            chosen_line = random.choice(valid_lines)
            print(f"{starting_player_name}: {chosen_line}!")

        # 역 이름 말하기
        print(f"\n<{chosen_line}>의 역 이름을 순서대로 말해주세요!")
        used_stations = []
        current_turn_index = start_index
        loser_name = ""

        while True:
            current_player = self.participants[current_turn_index]
            is_correct = False

            if current_player['name'] == self.player_name:
                answer = input(f"\n[{self.player_name}님 턴]: ").strip()
                if answer in used_stations:
                    print(f"❌ '{answer}'은/는 이미 나온 역입니다!")
                elif answer in Subway_Data[chosen_line]:
                    used_stations.append(answer)
                    is_correct = True
                else:
                    print(f"❌ '{answer}'은/는 {chosen_line}에 없는 역입니다!")
            else: # 컴퓨터 턴
                print(f"\n[{current_player['name']}님 턴...]")
                time.sleep(1.5)
                available = [s for s in Subway_Data[chosen_line] if s not in used_stations]
                if available and random.random() < 0.8: # 80% 확률로 정답
                    com_ans = random.choice(available)
                    print(f"{current_player['name']}: {com_ans}")
                    used_stations.append(com_ans)
                    is_correct = True
                else:
                    print(f"{current_player['name']}: ...모르겠다!")

            if not is_correct:
                loser_name = current_player['name']
                print(f"\n💥 {loser_name}님 당첨! 💥")
                # 패배자 처리
                for p in self.participants:
                    if p['name'] == loser_name:
                        p['drunk'] += 1
                        break
                
                print("\n--- 현재 상태 ---")
                for p in self.participants:
                    remain_limit = p['limit'] - p['drunk']
                    print(f" - {p['name']}: 마신 {p['drunk']}잔🍺, 남은 {remain_limit}잔🍺")
                
                return loser_name

            current_turn_index = (current_turn_index + 1) % len(self.participants)
    # ###################################
    
    # 게임을 시작하는 함수
    def start(self):
        # 순서 1. 인트로 2. 시작 여부 3. 이름 받기 4. 게임 종료
        self.intro()
        while True:
            yes_or_no = input("게임을 시작할까요?(y/n): ").strip().lower()
            if yes_or_no not in ('y', 'n'):
                print("y/n 중 골라주세요 ㅡㅡ : ")
                continue
            if yes_or_no == 'n':
                print("게임이 시작되지 못했습니다 ㅠ")
                return
            break
        self.player_name = input("오늘 거하게 취해볼 당신의 이름은? : ").strip()
        # self.participants.append(self.player_name)
        self.select_alcohol_limit()
        self.add_participant(self.player_name, self.alcohol_limit)
        
        self.invite_participants()
        self.show_game_list()
        self.play()


if __name__ == "__main__":
    try:
        game = alcohol_game()
        game.start()
    except Exception as e:
        print("오류 발생: ", e)
