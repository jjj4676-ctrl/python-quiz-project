import json
import os
import shutil

# 1. Quiz 클래스: 개별 퀴즈의 정보를 담는 틀
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        """객체 데이터를 딕셔너리로 변환 (JSON 저장용)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# 2. QuizGame 클래스: 게임의 전체 로직 제어
class QuizGame:
    def __init__(self):
        self.file_path = "state.json"
        self.quizzes = []
        self.high_score = 0
        self.load_data() # 시작 시 데이터 불러오기

    def get_default_quizzes(self):
        """최초 실행 시 사용할 기본 퀴즈 데이터셋"""
        return [
            Quiz("파이썬에서 리스트에 요소를 추가하는 함수는?", ["1) add()", "2) append()", "3) insert()", "4) push()"], 2),
            Quiz("파이썬의 주석 기호는?", ["1) //", "2) #", "3) /*", "4) --"], 2),
            Quiz("출력할 때 사용하는 함수는?", ["1) input()", "2) out()", "3) print()", "4) write()"], 3),
            Quiz("정수형 자료형은?", ["1) int", "2) str", "3) float", "4) bool"], 1),
            Quiz("나머지를 구하는 연산자는?", ["1) /", "2) //", "3) %", "4) **"], 3)
        ]

    def load_data(self):
        """파일에서 퀴즈와 최고 점수를 불러옵니다."""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 최고 점수 불러오기 (없으면 0)
                self.high_score = data.get("high_score", 0)
                # 퀴즈 목록 불러오기
                self.quizzes = [Quiz(q['question'], q['choices'], q['answer']) for q in data['quizzes']]
                print("[시스템] 데이터를 성공적으로 불러왔습니다.")

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # 파일이 없거나 데이터가 깨진 경우 초기 데이터 설정
            print("[알림] 기존 데이터가 없거나 손상되었습니다. 기본 설정을 로드합니다.")
            self.quizzes = self.get_default_quizzes()
            self.high_score = 0
            self.save_data()

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 파일에 저장합니다."""
        try:
            # 저장 전 백업 생성 (안정성 확보)
            if os.path.exists(self.file_path):
                shutil.copy(self.file_path, self.file_path + ".bak")

            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "high_score": self.high_score
            }
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"[시스템] 데이터가 '{self.file_path}'에 안전하게 저장되었습니다.")
        except Exception as e:
            print(f"[오류] 저장 중 문제가 발생했습니다: {e}")

    def start_game(self):
        """게임 시작 및 최고 점수 갱신 로직"""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        print("\n--- 퀴즈 게임 시작! ---")
        score = 0
        for q in self.quizzes:
            print(f"\n문제: {q.question}")
            for choice in q.choices:
                print(choice)
            
            # 정답 입력 및 범위 검증
            while True:
                try:
                    user_ans = int(input("정답 번호(1~4): "))
                    if 1 <= user_ans <= 4:
                        break
                    else:
                        print("⚠️ 1번에서 4번 사이의 번호를 입력하세요.")
                except ValueError:
                    print("⚠️ 숫자만 입력 가능합니다.")

            if user_ans == q.answer:
                print("✅ 정답입니다!")
                score += 20
            else:
                print(f"❌ 틀렸습니다. 정답은 {q.answer}번입니다.")

        print(f"\n[게임 종료] 이번 점수: {score}점")
        
        # 최고 점수 비교 및 갱신
        if score > self.high_score:
            print(f"🎊 축하합니다! 최고 기록을 경신했습니다! ({self.high_score} -> {score})")
            self.high_score = score
            self.save_data() # 점수 갱신 시 즉시 저장
        else:
            print(f"현재 최고 기록은 {self.high_score}점입니다. 다음 기회에 도전하세요!")

    def add_quiz(self):
        """새로운 퀴즈 추가 및 파일 저장"""
        print("\n--- 새 퀴즈 추가 ---")
        question = input("질문을 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choice = input(f"보기 {i}번 내용: ")
            choices.append(f"{i}) {choice}")
        
        while True:
            try:
                answer = int(input("정답 번호(1~4): "))
                if 1 <= answer <= 4:
                    self.quizzes.append(Quiz(question, choices, answer))
                    self.save_data() # 퀴즈 추가 시 즉시 저장
                    print("✅ 퀴즈가 성공적으로 추가되고 저장되었습니다!")
                    break
                else:
                    print("⚠️ 1~4 사이의 번호를 입력하세요.")
            except ValueError:
                print("⚠️ 숫자만 입력 가능합니다.")

    def show_quizzes(self):
        """등록된 모든 퀴즈 목록 출력"""
        print("\n--- 퀴즈 목록 ---")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def show_score(self):
        """현재 저장된 최고 점수 확인"""
        print(f"\n🏆 현재 최고 점수: {self.high_score}점")
        if self.high_score == 0:
            print("(아직 게임을 완료한 기록이 없습니다.)")

    def run(self):
        """메인 메뉴 루프"""
        while True:
            print("\n=== 파이썬 기초 퀴즈 프로그램 ===")
            print("1. 게임시작")
            print("2. 퀴즈추가")
            print("3. 퀴즈목록")
            print("4. 최고점수 확인")
            print("5. 종료")
            
            choice = input("선택: ")
            
            if choice == '1':
                self.start_game()
            elif choice == '2':
                self.add_quiz()
            elif choice == '3':
                self.show_quizzes()
            elif choice == '4':
                self.show_score()
            elif choice == '5':
                print("게임을 종료합니다. 이용해 주셔서 감사합니다!")
                break
            else:
                print("⚠️ 잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()