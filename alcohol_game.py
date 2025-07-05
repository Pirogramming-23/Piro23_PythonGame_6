import random
import time

class alcohol_game:
    def __init__(self):
        # 플레이어 이름
        self.name = ""
        self.alcohol_limit = 0
        self.game_list = []
    
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
            
            
    # 주량 선택
    def select_alcohol_limit(self):
        select = [2, 4, 6, 8, 10]
        alcohol_menu = (
            "-------------🍺소주 얼만큼 드세요(수줍)---{\\__/}----\n"
            "-------------1. 반병 (2잔)-------------(̷ ̷´̷ ̷^̷ ̷`̷)̷◞♡---\n"
            "-------------2. 반병에서 한병 (4잔)-----|  ⫘ |------\n"
            "-------------3. 한병에서 한병반 (6잔)-----|  ⫘ |------\n"
            "-------------4. 한병반에서 두병 (8잔)-----|  ⫘ |------\n"
            "-------------5. 두병 이상 (10잔)-----|  ⫘ |------\n"
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
    
    # 게임이 돌아가는 로직 구현
    def play(self):
        print(f"{self.name}님의 주량은 ({self.alcohol_limit}잔) 입니다.")
        
    
    # 게임을 시작하는 함수
    def start(self):
        # 순서 1. 인트로 2. 시작 여부 3. 이름 받기 4. 게임 종료
        self.intro()
        
        yes_or_no = input("게임을 시작할까요?(y/n): ").strip().lower()
        if yes_or_no not in ('y, n'):
            return print("y/n 중 골라주세요 ㅡㅡ : ")
        if yes_or_no == 'n':
            return print("게임이 시작되지 못했습니다 ㅠ")
        
        self.name = input("오늘 거하게 취해볼 당신의 이름은? : ").strip()
        self.game_list.append(self.name)
        print(f"참여자: {self.name}\n")
            
        self.select_alcohol_limit()
        self.play()

            
if __name__ == "__main__":
    game = alcohol_game()
    game.start()