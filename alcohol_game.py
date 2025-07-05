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
    
    # 게임이 돌아가는 로직 구현
    def play():
        print("게임 시작")
    
    # 게임을 시작하는 함수
    def start(self):
        # 순서 1. 인트로 2. 시작 여부 3. 이름 받기 4. 게임 종료
        self.intro()
        
        yes_or_no = input("게임을 시작할까요?(y/n): ")
        if yes_or_no == 'y' or yes_or_no == 'Y':
            self.name = input("오늘 거하게 취해볼 당신의 이름은? : ").strip()
            self.game_list.append(self.name)
            
            self.play()
        else:
            print("게임이 시작되지 못했습니다 ㅠ")
            
if __name__ == "__main__":
    game = alcohol_game()
    game.start()