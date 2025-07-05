import random
import time

class alcohol_game:
    def __init__(self):
        # 플레이어 이름
        self.player_name = ""
        self.alcohol_limit = 0
        self.game_list = {"아파트":self.apartment_game}
        self.player_names = []
        self.participants = []
    
    # 인트로 함수 너무 빨리 출력된다고 생각들면 추후 sleep 시간 조정가능
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
            "-------------1. 반병 (2잔)---------------(̷ ̷´̷ ̷^̷ ̷`̷)̷◞♡---\n"
            "-------------2. 반병에서 한병 (4잔)------|  ⫘ |------\n"
            "-------------3. 한병에서 한병반 (6잔)------------------\n"
            "-------------4. 한병반에서 두병 (8잔)------------------\n"
            "-------------5. 두병 이상 (10잔)----------------------\n"
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
        participants = ["은서","하연","연서","예진"]
        
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
        for p in self.participants:
            remain_limit = p['limit'] - p['drunk']
            print(f" - {p['name']}: 마신 {p['drunk']}잔, 남은 {remain_limit}잔")

        print("\n참가자 리스트:")
        print(", ".join(self.player_names), "\n")
        
        
    # 게임이 돌아가는 로직 구현
    def play(self):
        print(f"{self.player_name}님의 주량은 ({self.alcohol_limit}잔) 입니다.")
        while True:
            
            # 게임 리스트
            for i, game_name in enumerate(self.game_list.keys(), start=1):
                print(f"{i}. {game_name}")
            
            select = input("게임을 골라주세요: ").strip()
            
            try:
                game_keys = list(self.game_list.keys())
                selected_game = game_keys[int(select)-1]
                print(f"\n{selected_game} 게임을 시작!\n")
                self.game_list[selected_game]()
            except(ValueError, IndexError):
                print("숫자를 입력해주세요 잘못 입력했습니다.")
                continue
            
            for i in self.participants:
                if i['drunk'] >= i['limit']:
                    print(f"\n{i['name']}님이 치사량을 넘겼습니다")
                    return
            
            keep_going = input("다음 게임 계속 하실까요?(y/n): ").strip().lower()
            if keep_going != 'y':
                print("\n게임 종료!")
                break
        
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

    def apartment_game(self):
        print("\n 아파트~~!, 아파트~~!, 아파트~~!, uh, uh-huh, uh-huh [...대충 부르노 마스 보컬]")
        
        # 참가자는 손이 2개이다
        hands = []
        for i in self.participants:
            hands += [i['name'], i['name']]
        total_hands = len(hands)
        print(f"총 손 개수 : {total_hands}개 ({len(self.participants)}명 x 2손)\n")
        
        while True:
            try:
                floor = int(input("몇 층에 사세요?: ").strip())
                break
            except ValueError:
                print("숫자만 입력해주세요")
        
        idx = (floor - 1) % total_hands
        loser = hands[idx]
        
        for i in self.participants:
            if i['name'] == loser:
                i['drunk'] += 1
                print(f"\n {loser}님이 {floor}층에서 탈락!!!")
                print(f"   → 현재 마신 잔: {i['drunk']}잔 (주량 대비 {i['limit'] - i['drunk']}잔 남음)\n")
                break
        
    # ###############################
    
    
    
    
    
    
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
    game = alcohol_game()
    game.start()