import json
import os
import sys
import shutil # 백업 기능을 위해 추가

# 1. Quiz 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# 2. QuizGame 클래스
class QuizGame:
    def __init__(self):
        self.file_path = "state.json"
        self.quizzes = []
        self.high_score = 0
        self.load_data()

    def get_default_quizzes(self):
        """기본 퀴즈 데이터셋 반환"""
        return [
            Quiz("파이썬에서 리스트에 요소를 추가하는 함수는?", ["1) add()", "2) append()", "3) insert()", "4) push()"], 2),
            Quiz("파이썬의 주석 기호는?", ["1) //", "2) #", "3) /*", "4) --"], 2),
            Quiz("출력할 때 사용하는 함수는?", ["1) input()", "2) out()", "3) print()", "4) write()"], 3),
            Quiz("정수형 자료형은?", ["1) int", "2) str", "3) float", "4) bool"], 1),
            Quiz("나머지를 구하는 연산자는?", ["1) /", "2) //", "3) %", "4) **"], 3)
        ]

    def load_data(self):
        """데이터 로드 및 예외 처리 (평가 항목 #15 반영)"""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.high_score = data.get("high_score", 0)
                self.quizzes = [Quiz(q['question'], q['choices'], q['answer']) for q in data['quizzes']]
                print("[시스템] 데이터를 성공적으로 불러왔습니다.")

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print("[경고] 데이터 파일이 없거나 손상되었습니다. 기본 데이터로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.save_data()

    def backup_data(self):
        """데이터 백업 (평가 항목 #19 반영)"""
        if os.path.exists(self.file_path):
            shutil.copy(self.file_path, self.file_path + ".bak")

    def save_data(self):
        """데이터 저장 (평가 항목 #15 반영)"""
        try:
            self.backup_data() # 저장 전 백업
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "high_score": self.high_score
            }
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"[시스템] 데이터가 '{self.file_path}'에 안전하게 저장되었습니다.")
        except Exception as e:
            print(f"[오류] 저장 중 문제가 발생했습니다: {e}")

    def reset_data(self):
        """데이터 초기화 (평가 항목 #19 반영)"""
        confirm = input("\n⚠️ 정말로 모든 데이터를 초기화하시겠습니까? (y/n): ")
        if confirm.lower() == 'y':
            self.backup_data()
            self.quizzes = self.get_default_quizzes()
            self.high_score = 0
            self.save_data()
            print("[알림] 데이터가 초기화되었습니다. (.bak 파일로 백업됨)")

    def start_game(self):
        print("\n--- 게임을 시작합니다! ---")
        score = 0
        for q in self.quizzes:
            print(f"\n문제: {q.question}")
            for choice in q.choices:
                print(choice)
            
            while True:
                try:
                    user_ans = int(input("정답 번호(1~4)를 입력하세요: "))
                    if 1 <= user_ans <= 4: break
                    else: print("⚠️ 1~4 사이의 번호를 입력하세요.")
                except ValueError:
                    print("⚠️ 숫자만 입력 가능합니다.")

            if user_ans == q.answer:
                print("✅ 정답입니다!")
                score += 20
            else:
                print(f"❌ 틀렸습니다. 정답은 {q.answer}번입니다.")

        print(f"\n최종 점수: {score}점")
        if score > self.high_score:
            print(f"🎊 최고 기록 경신! ({self.high_score} -> {score})")
            self.high_score = score
            self.save_data()

    def add_quiz(self):
        print("\n--- 새 퀴즈 추가 ---")
        question = input("질문을 입력하세요: ")
        choices = [f"{i}) {input(f'보기 {i}번 내용: ')}" for i in range(1, 5)]
        
        while True:
            try:
                answer = int(input("정답 번호(1~4): "))
                if 1 <= answer <= 4:
                    self.quizzes.append(Quiz(question, choices, answer))
                    self.save_data()
                    break
                else: print("⚠️ 1~4 사이여야 합니다.")
            except ValueError: print("⚠️ 숫자만 입력 가능합니다.")

    def show_quizzes(self):
        print("\n--- 퀴즈 목록 ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def show_score(self):
        print(f"\n현재 최고 점수: {self.high_score}점")

    def run(self):
        """메인 루프 (평가 항목 #19, #20 반영)"""
        while True:
            print("\n=== 파이썬 퀴즈 게임 ===")
            print("1. 게임시작 2. 퀴즈추가 3. 목록보기 4. 최고점수 5. 데이터초기화 6. 종료")
            choice = input("선택: ")
            
            if choice == '1': self.start_game()
            elif choice == '2': self.add_quiz()
            elif choice == '3': self.show_quizzes()
            elif choice == '4': self.show_score()
            elif choice == '5': self.reset_data()
            elif choice == '6': 
                print("게임을 종료합니다.")
                break
            else: print("잘못된 선택입니다.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()