import json

class Question:
    def __init__(self, prompt, options, answer):
        self.prompt = prompt
        self.options = options
        self.answer = answer

class QuizManager:
    def __init__(self):
        self.questions = []
        self.load_questions()

    def load_questions(self):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.questions = [Question(q['prompt'], q['options'], q['answer']) for q in data]
        except FileNotFoundError:
            self.questions = []

    def save_questions(self):
        """퀴즈 목록을 JSON 파일에 저장 (추가 기능용)"""
        data = [{"prompt": q.prompt, "options": q.options, "answer": q.answer} for q in self.questions]
        with open("questions.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_quiz(self):
        """새로운 퀴즈 추가 기능 (2단계 요구사항)"""
        prompt = input("문제 내용을 입력하세요: ")
        options = [input(f"{i+1}번 선택지: ") for i in range(4)]
        answer = int(input("정답 번호(1~4): "))
        self.questions.append(Question(prompt, options, answer))
        self.save_questions()
        print("✅ 문제가 추가되었습니다!")

    def list_quizzes(self):
        """퀴즈 목록 조회 기능 (2단계 요구사항)"""
        print("\n--- 퀴즈 목록 ---")
        for i, q in enumerate(self.questions):
            print(f"{i+1}. {q.prompt}")

    def start_game(self):
        # ... (기존 게임 시작 로직과 동일)
        score = 0
        for q in self.questions:
            print(f"\n{q.prompt}")
            for opt in q.options: print(opt)
            ans = int(input("답: "))
            if ans == q.answer: score += 1
        print(f"최종 점수: {score}/{len(self.questions)}")

# main 함수에 메뉴 추가 (추가, 목록 조회)
def main():
    manager = QuizManager()
    while True:
        print("\n1.게임시작 2.퀴즈추가 3.퀴즈목록 4.종료")
        choice = input("선택: ")
        if choice == '1': manager.start_game()
        elif choice == '2': manager.add_quiz()
        elif choice == '3': manager.list_quizzes()
        elif choice == '4': break