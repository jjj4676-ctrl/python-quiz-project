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
        """questions.json에서 문제 로드"""
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.questions = [Question(q['prompt'], q['options'], q['answer']) for q in data]
        except FileNotFoundError:
            print("\n❌ 오류: questions.json 파일이 없습니다.")

    def save_score(self, name, score):
        """점수를 rankings.json에 저장"""
        rankings = []
        try:
            with open("rankings.json", "r", encoding="utf-8") as f:
                rankings = json.load(f)
        except FileNotFoundError:
            pass # 파일이 없으면 새로 만듭니다.

        rankings.append({"name": name, "score": score})
        # 점수 높은 순으로 정렬
        rankings = sorted(rankings, key=lambda x: x['score'], reverse=True)

        with open("rankings.json", "w", encoding="utf-8") as f:
            json.dump(rankings, f, ensure_ascii=False, indent=4)
        print("\n✅ 점수가 저장되었습니다!")

    def show_rankings(self):
        """저장된 랭킹 출력"""
        try:
            with open("rankings.json", "r", encoding="utf-8") as f:
                rankings = json.load(f)
            print("\n🏆 --- 현재 랭킹 TOP 5 ---")
            for i, r in enumerate(rankings[:5]): # 상위 5명만 출력
                print(f"{i+1}위: {r['name']} - {r['score']}점")
        except FileNotFoundError:
            print("\n아직 등록된 랭킹이 없습니다. 첫 주인공이 되어보세요!")

    def start_game(self):
        if not self.questions:
            print("문제가 없어 게임을 시작할 수 없습니다.")
            return

        print("\n--- 게임 시작! ---")
        score = 0
        for i, q in enumerate(self.questions):
            print(f"\n문제 {i+1}: {q.prompt}")
            for opt in q.options: print(opt)
            
            try:
                ans = int(input("답: "))
                if ans == q.answer:
                    print("정답! ✨")
                    score += 1
                else:
                    print(f"오답! 정답은 {q.answer}번.")
            except ValueError:
                print("숫자만 입력하세요.")

        print(f"\n최종 점수: {score}/{len(self.questions)}")
        name = input("이름을 입력하세요: ")
        self.save_score(name, score)

def main():
    manager = QuizManager()
    while True:
        print("\n--- 파이썬 퀴즈 게임 ---")
        print("1. 게임 시작  2. 랭킹 보기  3. 종료")
        choice = input("선택: ")
        
        if choice == '1':
            manager.start_game()
        elif choice == '2':
            manager.show_rankings()
        elif choice == '3':
            print("안녕히 가세요!")
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()