import json
import os
import sys # 시스템 종료를 위해 추가

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

    def load_data(self):
        """파일 읽기 예외 처리 강화 (종합 평가 반영)"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
            except (json.JSONDecodeError, KeyError):
                # 파일이 깨져있거나 형식이 잘못된 경우 처리
                print("⚠️ 데이터 파일이 손상되어 초기화합니다.")
                self.quizzes = []
                self.high_score = 0
        
        if not self.quizzes:
            self.quizzes = [
                Quiz("파이썬에서 리스트에 요소를 추가하는 함수는?", ["1) add()", "2) append()", "3) insert()", "4) push()"], 2),
                Quiz("파이썬의 주석 기호는?", ["1) //", "2) #", "3) /*", "4) --"], 2),
                Quiz("출력할 때 사용하는 함수는?", ["1) input()", "2) out()", "3) print()", "4) write()"], 3),
                Quiz("정수형 자료형은?", ["1) int", "2) str", "3) float", "4) bool"], 1),
                Quiz("나머지를 구하는 연산자는?", ["1) /", "2) //", "3) %", "4) **"], 3)
            ]
            self.save_data()

    def save_data(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "high_score": self.high_score
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def start_game(self):
        """정답 입력 범위 검증 로직 추가 (평가 항목 #2 반영)"""
        print("\n--- 게임을 시작합니다! ---")
        score = 0
        for q in self.quizzes:
            print(f"\n문제: {q.question}")
            for choice in q.choices:
                print(choice)
            
            # ✅ 수정 포인트: 올바른 범위의 숫자를 입력할 때까지 무한 루프
            while True:
                try:
                    user_ans = int(input("정답 번호(1~4)를 입력하세요: "))
                    if 1 <= user_ans <= 4:
                        break # 올바른 범위면 반복 탈출
                    else:
                        print("⚠️ 1번부터 4번 사이의 번호를 선택해주세요.")
                except ValueError:
                    print("⚠️ 숫자만 입력 가능합니다. 다시 시도하세요.")

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
        """퀴즈 추가 시에도 범위 검증 적용"""
        print("\n--- 새 퀴즈 추가 ---")
        question = input("질문을 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choice = input(f"보기 {i}번 내용을 입력하세요: ")
            choices.append(f"{i}) {choice}")
        
        # ✅ 수정 포인트: 정답 번호 입력 시에도 범위 검증 추가
        while True:
            try:
                answer = int(input("정답 번호(1~4)를 입력하세요: "))
                if 1 <= answer <= 4:
                    self.quizzes.append(Quiz(question, choices, answer))
                    self.save_data()
                    print("퀴즈가 성공적으로 추가되었습니다!")
                    break
                else:
                    print("⚠️ 정답 번호는 1에서 4 사이여야 합니다.")
            except ValueError:
                print("⚠️ 숫자만 입력 가능합니다.")

    def show_quizzes(self):
        print("\n--- 퀴즈 목록 ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def show_score(self):
        print(f"\n현재 최고 점수: {self.high_score}점")

    def run(self):
        """비정상 종료(Ctrl+C) 예외 처리 추가 (종합 평가 반영)"""
        try:
            while True:
                print("\n=== 파이썬 기초 퀴즈 게임 ===")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록")
                print("4. 최고 점수 확인")
                print("5. 종료")
                
                choice = input("메뉴를 선택하세요: ")
                if choice == '1': self.start_game()
                elif choice == '2': self.add_quiz()
                elif choice == '3': self.show_quizzes()
                elif choice == '4': self.show_score()
                elif choice == '5':
                    print("게임을 종료합니다.")
                    break
                else:
                    print("잘못된 선택입니다.")
        except KeyboardInterrupt:
            # Ctrl+C를 눌렀을 때 프로그램이 깨지지 않고 우아하게 종료되도록 함
            print("\n\n👋 사용자에 의해 프로그램이 강제 종료되었습니다.")
            sys.exit(0)

if __name__ == "__main__":
    game = QuizGame()
    game.run()