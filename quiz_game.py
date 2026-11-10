class Question:
    """퀴즈 문제 하나에 대한 정보를 담는 클래스"""
    def __init__(self, prompt, options, answer):
        self.prompt = prompt    # 질문 내용
        self.options = options  # 보기 (리스트)
        self.answer = answer    # 정답 번호 (1, 2, 3, 4)

class QuizManager:
    """전체 퀴즈 게임을 관리하는 클래스"""
    def __init__(self):
        self.questions = []  # 문제들을 담을 리스트
        self.score = 0       # 현재 점수
        self.load_questions()

    def load_questions(self):
        # 테스트용 문제를 미리 추가합니다.
        q1 = Question("파이썬의 창시자는 누구일까요?", 
                      ["1. 귀도 반 로섬", "2. 제임스 고슬링", "3. 빌 게이츠", "4. 스티브 잡스"], 1)
        q2 = Question("파이썬에서 리스트에 요소를 추가하는 함수는?", 
                      ["1. add()", "2. append()", "3. push()", "4. insert_all()"], 2)
        self.questions.append(q1)
        self.questions.append(q2)

    def start_game(self):
        print("\n--- 게임을 시작합니다! ---")
        self.score = 0
        for i, q in enumerate(self.questions):
            print(f"\n문제 {i+1}: {q.prompt}")
            for option in q.options:
                print(option)
            
            try:
                user_answer = int(input("정답 번호를 입력하세요: "))
                if user_answer == q.answer:
                    print("정답입니다! ✨")
                    self.score += 1
                else:
                    print(f"틀렸습니다. 정답은 {q.answer}번입니다. 😢")
            except ValueError:
                print("숫자만 입력 가능합니다. 이번 문제는 오답 처리됩니다.")
        
        print(f"\n게임 종료! 당신의 점수는 {self.score}/{len(self.questions)}입니다.")

def main():
    manager = QuizManager() # 퀴즈 매니저 생성
    
    while True:
        print("\n--- 파이썬 퀴즈 게임 ---")
        print("1. 게임 시작")
        print("2. 랭킹 보기 (준비 중)")
        print("3. 종료")
        
        choice = input("메뉴를 선택하세요: ")
        
        if choice == '1':
            manager.start_game() # 매니저를 통해 게임 시작
        elif choice == '2':
            print("현재 랭킹 기능은 개발 중입니다.")
        elif choice == '3':
            print("게임을 종료합니다. 안녕!")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 골라주세요.")

if __name__ == "__main__":
    main()
    