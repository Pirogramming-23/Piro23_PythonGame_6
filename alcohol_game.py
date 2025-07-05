import random
import time

class alcohol_game:
    def __init__(self):
        # 플레이어 이름
        self.name = ""
        self.alcohol_limit = 0
        self.game_list = []
    
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
            
    def start(self):
        self.intro()
        
game = alcohol_game()
game.start()