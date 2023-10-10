from db import session, Test, Question, Answer, User
from datetime import datetime, time


class AdminTestManager:
    @staticmethod
    def create_test(name, description, questions_data):
        test = Test(name=name, description=description)
        session.add(test)
        session.commit()

        for question_text, answers in questions_data:
            question = Question(text=question_text, test_id=test.id)
            session.add(question)
            session.commit()

            for answer_text, is_correct in answers:
                answer = Answer(text=answer_text, is_correct=is_correct, question_id=question.id)
                session.add(answer)

        session.commit()
        return test

    @staticmethod
    def get_tests():
        return session.query(Test)

    @staticmethod
    def delete_test(test_id):
        test = session.query(Test).filter_by(id=test_id).first()
        if test:
            session.delete(test)
            session.commit()
            return True
        return False

    @staticmethod
    def test_exists(test_name):
        return True if session.query(Test).filter_by(name=test_name).first() else False

class UserTestManager:
    @staticmethod
    def start_test(test_id):
        test = session.query(Test).filter_by(id=test_id).first()
        if test:
            user = User(test_id=test_id, start_time=datetime.now())
            session.add(user)
            session.commit()
            return user
        return None

    @staticmethod
    def finish_test(user_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.end_time = datetime.now()
            session.commit()
            return user
        return None

    @staticmethod
    def get_user_choice_by_options(options, options_check, user):
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        while True:
            try:
                choice = int(input("Оберіть номер відповіді: "))
                if 1 <= choice <= len(options):
                    if options_check[choice-1]:
                        user.score += 1
                        session.commit()
                    return choice
                else:
                    print("Будь ласка, оберіть правильный номер.")
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")

    @staticmethod
    def get_user_choice(option_check, user):
        while True:
            try:
                choice = input("Напишіть відповідь: ")
                if option_check[0].lower() == choice.lower():
                    user.score += 1
                    session.commit()
                    return choice
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")
