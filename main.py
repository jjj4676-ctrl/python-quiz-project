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
        """state.json에서 데이터를 불러오고 성공/실패 로그를 남깁니다."""
        if os.path.exists(self.file_path):
            try:
            if not os.path.exists('state.json'):
                raise FileNotFoundError # 파일이 없으면 예외 발생시켜 except문으로 유도
            
            with open('state.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 데이터 변환 로직...
                print("[시스템] 데이터를 성공적으로 불러왔습니다.")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            # 파일이 없거나 내용이 깨진 경우(JSONDecodeError) 실행
            print(f"[경고] 데이터 파일 로드 실패({type(e).__name__}). 기본 데이터로 복구합니다.")
            self.quizzes = self.get_default_quizzes() # 기본 데이터셋 로드
            self.save_data() # 복구된 상태를 파일로 다시 저장

        # 기본 퀴즈 생성 로직 (기존과 동일)
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
        """현재 상태를 state.json에 저장하고 성공/실패 로그를 남깁니다."""
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "high_score": self.high_score
            }
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            # ✅ 성공 로그: 저장이 완료되었음을 알림
            print(f"[시스템] 데이터 저장 완료: '{self.file_path}'에 안전하게 기록되었습니다.")
            
        except PermissionError:
            # ❌ 실패 로그: 권한 문제 등 특정 상황 명시
            print("[시스템/에러] 데이터 저장 실패: 파일 쓰기 권한이 없습니다.")
        except Exception as e:
            # ❌ 실패 로그: 기타 에러 발생 시 복구를 위해 에러 내용 출력
            print(f"[시스템/에러] 데이터 저장 중 오류 발생: {e}")

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
        try:
            while True:
                # 기존 메뉴 출력 및 선택 로직
                choice = self.display_menu()
                if choice == '5':
                    self.save_data()
                    print("게임을 종료합니다.")
                    break
                # ... 나머지 메뉴 처리 ...
        
        # [보완 사항] 비정상 종료(Ctrl+C, Ctrl+D) 대응
        except (KeyboardInterrupt, EOFError):
            print("\n\n[알림] 사용자에 의해 프로그램이 강제 종료되었습니다.")
            self.save_data()  # 종료 전 자동 저장
            print("현재까지의 데이터를 안전하게 저장하고 종료합니다.")

def backup_data(self):
        """데이터 저장 전 백업 파일 생성 (평가 항목 #19 반영)"""
        try:
            if os.path.exists('state.json'):
                shutil.copy('state.json', 'state.json.bak')
                # print("[시스템] 백업 파일(state.json.bak)이 생성되었습니다.")
        except Exception as e:
            print(f"[경고] 백업 생성 실패: {e}")

    def reset_data(self):
        """데이터 초기화 및 기존 데이터 백업 (평가 항목 #19 반영)"""
        confirm = input("정말로 모든 데이터를 초기화하시겠습니까? (y/n): ")
        if confirm.lower() == 'y':
            self.backup_data() # 초기화 전 현재 상태 백업
            self.quizzes = self.get_default_quizzes() # 기본값으로 교체
            self.save_data()
            print("[알림] 데이터가 초기화되었습니다. (이전 데이터는 .bak 파일에 보관됨)")

if __name__ == "__main__":
    game = QuizGame()
    game.run()