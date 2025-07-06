import random
import time

class alcohol_game:
    def __init__(self):
        # 플레이어 이름
        self.player_name = ""
        self.alcohol_limit = 0
        self.game_list = ["딸기게임", "369게임"]
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
            self.show_game_list()
            choice = input("어떤 게임을 플레이할까요? 번호를 입력해주세요 (종료하려면 q): ").strip()

            if choice == 'q':
                print("게임을 종료합니다. 안녕히 가세요~ 🍻")
                break

            if choice == '1':
                print("딸기게임은 아직 준비 중이에요. 다음에 만나요!\n")
            elif choice == '2':
                self.game_369()
            else:
                print("잘못된 선택입니다. 다시 입력해주세요.\n")

        

    # 게임 리스트 함수
    def show_game_list(self):
        print("\n 게임 리스트")
        if not self.game_list:
            print("게임이 없는뎁쇼?!?!?")
        else:
            for i, game in enumerate(self.game_list, start=1):
                print(f"{i}. {game}\n")


    # 369 게임 함수
    def game_369(self):
        print("369 게임을 시작합니다! 3, 6, 9가 들어간 숫자는 '짝'을 외쳐주세요!")
        print("---369! 369! 369! 369!---")

        current_num = 1
        turn = 0

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
                answer = input(f"{name}의 차례: ").strip()
            else:
                is_correct = random.random() < 0.8
                if is_correct:
                    answer = expected
                else:
                    if expected == "짝":
                        answer = str(current_num)
                    else:
                        answer = "짝"
                print(f"{name}의 차례: {answer}")

            if answer != expected:
                player['drunk'] += 1
                remain = player['limit'] - player['drunk']

                print(f"{name} 틀렸습니다! ➤ 한 잔 마십니다!\n")
                break
            
            current_num += 1
            turn += 1


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