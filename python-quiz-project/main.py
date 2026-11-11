import json
import os

# 1. Quiz 클래스: 퀴즈 하나에 대한 질문, 보기, 정답 정보를 담는 클래스입니다.
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question  # 퀴즈 질문
        self.choices = choices    # 4지선다형 보기 (리스트)
        self.answer = answer      # 정답 번호 (1-4)

    def to_dict(self):
        """객체 데이터를 딕셔너리로 변환 (JSON 저장용)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# 2. QuizGame 클래스: 게임의 전체 로직을 관리합니다.
class QuizGame:
    """
    퀴즈 게임의 전체적인 로직(데이터 로드, 게임 실행, 저장 등)을 관리하는 클래스입니다.
    """
    def __init__(self):
        self.file_path = "state.json"
        self.quizzes = []
        self.high_score = 0
        self.load_data()

    def load_data(self):
        """state.json에서 데이터 불러오기"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.high_score = data.get("high_score", 0)
                # 저장된 딕셔너리 리스트를 Quiz 객체 리스트로 변환
                self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
        
        # 만약 불러온 퀴즈가 없다면 기본 퀴즈 5개 생성
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
        """현재 상태를 state.json에 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "high_score": self.high_score
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def start_game(self):
        """퀴즈 풀기 기능"""
        print("\n--- 게임을 시작합니다! ---")
        score = 0
        for q in self.quizzes:
            print(f"\n문제: {q.question}")
            for choice in q.choices:
                print(choice)
            
            try:
                user_ans = int(input("정답 번호를 입력하세요: "))
                if user_ans == q.answer:
                    print("✅ 정답입니다!")
                    score += 20
                else:
                    print(f"❌ 틀렸습니다. 정답은 {q.answer}번입니다.")
            except ValueError:
                print("숫자만 입력해주세요. 이번 문제는 틀린 것으로 간주합니다.")

        print(f"\n최종 점수: {score}점")
        if score > self.high_score:
            print(f"🎊 최고 기록 경신! ({self.high_score} -> {score})")
            self.high_score = score
            self.save_data()

    def add_quiz(self):
        """새로운 퀴즈 추가 기능"""
        print("\n--- 새 퀴즈 추가 ---")
        question = input("질문을 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choice = input(f"보기 {i}번 내용을 입력하세요: ")
            choices.append(f"{i}) {choice}")
        
        try:
            answer = int(input("정답 번호(1~4)를 입력하세요: "))
            self.quizzes.append(Quiz(question, choices, answer))
            self.save_data()
            print("퀴즈가 성공적으로 추가되었습니다!")
        except ValueError:
            print("잘못된 입력입니다. 추가 실패.")

    def show_quizzes(self):
        """등록된 퀴즈 목록 보기"""
        print("\n--- 퀴즈 목록 ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def show_score(self):
        """최고 점수 확인"""
        print(f"\n현재 최고 점수: {self.high_score}점")

    def run(self):
        """메뉴 시스템"""
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

if __name__ == "__main__":
    game = QuizGame()
    game.run()