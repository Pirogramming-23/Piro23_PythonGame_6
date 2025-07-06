import random
import time
import pandas as pd
import re

class alcohol_game:
    def __init__(self):
        self.player_name = ""
        self.alcohol_limit = 0
        self.game_list = ["딸기게임", "369게임", "끝말잇기"]
        self.player_names = []
        self.participants = []
        self.word_list = self.extract_nouns_from_csv("/content/kr_korean.csv")

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

    def is_clean_korean(self, word):
        return bool(re.fullmatch(r'[가-힣]{2,}', str(word)))

    def extract_nouns_from_csv(self, path):
        try:
            df = pd.read_csv(path, encoding='utf-8')
            noun_df = df[df['어미'].str.contains('명사', na=False)]
            clean_nouns = noun_df['-가'].dropna().drop_duplicates()
            return [word for word in clean_nouns if self.is_clean_korean(word)]
        except Exception as e:
            print(f"CSV 불러오기 실패: {e}")
            return []

    def add_participant(self, name, limit):
        self.participants.append({'name': name, 'limit': limit, 'drunk': 0})
        self.player_names.append(name)

    def select_alcohol_limit(self):
        select = [2, 4, 6, 8, 10]
        alcohol_menu = (
            "-------------🍺소주 얼만큼 드세요---\n"
            "-------------1. 반병 (2잔)\n"
            "-------------2. 반병~한병 (4잔)\n"
            "-------------3. 한병~한병반 (6잔)\n"
            "-------------4. 한병반~두병 (8잔)\n"
            "-------------5. 두병 이상 (10잔)\n"
        )
        while True:
            print(alcohol_menu)
            choice = input("당신의 치사량을 선택하세요(1~5): ").strip()
            if choice in ('1', '2', '3', '4', '5'):
                self.alcohol_limit = select[int(choice) - 1]
                print(f"> 설정된 주량: {self.alcohol_limit}잔\n")
                break
            else:
                print("잘못 선택했습니다. 다시 골라주세요\n")

    def invite_participants(self):
        participants = ["은서", "하연", "연서", "예진"]
        while True:
            try:
                n = int(input("초대할 사람 수(최대 3명): ").strip())
                if 0 <= n <= 3:
                    break
            except ValueError:
                pass
            print("3명까지만 불러주세요.")
        chosen = random.sample(participants, n)
        for p in chosen:
            limit = random.choice([2, 4, 6, 8, 10])
            self.add_participant(p, limit)

        print("\n현재 상태:")
        for p in self.participants:
            print(f" - {p['name']}: 마신 {p['drunk']}잔, 남은 {p['limit'] - p['drunk']}잔")

        print("\n참가자 리스트:")
        print(", ".join(self.player_names), "\n")

    def get_computer_word(self, last_char, used_words):
        for word in self.word_list:
            if word.startswith(last_char) and word not in used_words:
                return word
        return None

    def play_end_word_game(self):
        used_words = []
        last_char = None

        print("\n끝말잇기를 시작합니다. '끝'을 입력하면 종료됩니다.")
        print("2글자 이상 순수 한글 단어만 사용할 수 있습니다.\n")

        while True:
            user_word = input("당신의 단어: ").strip()
            if user_word == "끝":
                print("게임을 종료합니다.")
                break
            if len(user_word) < 2:
                print("2글자 이상 입력하세요.")
                continue
            if user_word in used_words:
                print("이미 사용된 단어입니다. 당신이 졌습니다.")
                break
            if user_word not in self.word_list:
                print("사전에 없는 단어입니다. 다시 입력하세요.")
                continue
            if last_char and not user_word.startswith(last_char):
                print(f"'{last_char}'로 시작해야 합니다.")
                continue

            used_words.append(user_word)
            last_char = user_word[-1]

            comp_word = self.get_computer_word(last_char, used_words)
            if comp_word:
                print(f"컴퓨터: {comp_word}")
                used_words.append(comp_word)
                last_char = comp_word[-1]
            else:
                print("컴퓨터가 단어를 못 찾았습니다. 당신이 이겼습니다!")
                break

    def play(self):
        print(f"{self.player_name}님의 주량은 {self.alcohol_limit}잔입니다.\n")
        while True:
            self.show_game_list()
            choice = input("플레이할 게임 번호를 선택하세요 (종료: q): ").strip()
            if choice == 'q':
                print("게임 종료!")
                break
            elif choice == '3':
                self.play_end_word_game()
            else:
                print("아직 구현되지 않은 게임입니다. 다른 게임을 선택하세요.\n")

    def show_game_list(self):
        print("\n게임 리스트:")
        for i, game in enumerate(self.game_list, start=1):
            print(f"{i}. {game}")

    def start(self):
        self.intro()
        while True:
            yn = input("게임을 시작할까요? (y/n): ").strip().lower()
            if yn == 'y':
                break
            elif yn == 'n':
                print("게임을 시작하지 않았습니다.")
                return
            else:
                print("y 또는 n만 입력해주세요.")

        self.player_name = input("당신의 이름은? : ").strip()
        self.select_alcohol_limit()
        self.add_participant(self.player_name, self.alcohol_limit)
        self.invite_participants()
        self.play()


if __name__ == "__main__":
    game = alcohol_game()
    game.start()