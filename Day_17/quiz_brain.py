import os
class QuizBrain:
    def __init__(self, q_list):
        self.q_n = 0
        self.q_l = q_list
        self.score=0

    def still_has_questions(self):
        if self.q_n < len(self.q_l):
            return True
        else:
            False

    def next_question(self):
        current_question = self.q_l[self.q_n]
        self.q_n += 1
        user_answer = input(f"{self.q_n}: {current_question.text}(true/false)")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("You get it right")
        else:
            print("That's wrong")
        print(f"The correct answer was: {correct_answer}")
        print(f"Your current score is: {self.score}/{self.q_n}")


