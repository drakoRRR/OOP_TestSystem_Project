from db import session, Test, Question, Answer, User, Types
from datetime import datetime

from project_test.bases.question_base import QuestionOptions, QuestionUserBlank, QuestionFewOptions, QuestionTrueFalse
from project_test.bases.search_test_base import SearchTestByName, SearchTestByDescription


class AdminTestManager:
    @staticmethod
    def create_test(name, description, questions_data):
        '''Логіка створення тесту'''

        test = Test(name=name, description=description)
        session.add(test)
        session.commit()

        for question_text, answers, question_type in questions_data:
            question = Question(text=question_text,
                                test_id=test.id,
                                type_id=session.query(Types.id).filter_by(type_question=question_type).scalar())
            session.add(question)
            session.commit()

            for answer_text, is_correct in answers:
                answer = Answer(text=answer_text, is_correct=is_correct, question_id=question.id)
                session.add(answer)

        session.commit()
        return test

    @staticmethod
    def get_tests():
        '''Геттер для тестів'''

        return session.query(Test)

    @staticmethod
    def delete_test(test_id):
        '''Логіка видалення тесту'''

        test = session.query(Test).filter_by(id=test_id).first()
        if test:
            session.delete(test)
            session.commit()
            return True
        return False

    @staticmethod
    def test_exists(test_name):
        '''Перевірка чи існує тест'''

        return True if session.query(Test).filter_by(name=test_name).first() else False

class UserTestManager:
    @staticmethod
    def start_test(test_id):
        '''Початок тесту де ми засікаємо наш час проходження'''

        test = session.query(Test).filter_by(id=test_id).first()
        if test:
            user = User(test_id=test_id, start_time=datetime.now())
            session.add(user)
            session.commit()
            return user
        return None

    @staticmethod
    def finish_test(user_id):
        '''Кінець тесту де закінчуємо наш відлік часу'''

        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.end_time = datetime.now()
            session.commit()
            return user
        return None

    @staticmethod
    def get_user_choice_by_options(options, options_check, user):
        '''Логіка відповіді з 2 і більше варіантами відповіді і лише одним правильним варіантом'''
        QuestionOptions.get_answers_for_question(options)
        QuestionOptions.get_user_choice(options, options_check, user)

    @staticmethod
    def get_user_choice(option_check, user):
        '''Логіка відповіді де користувач сам вводить дані'''

        QuestionUserBlank.get_user_choice(option_check, user)

    @staticmethod
    def get_user_few_choices(options, options_check, user):
        '''Логіка відповіді з 2 і більше варіантами відповіді і декількома правильними варінтами'''

        QuestionFewOptions.get_answers_for_question(options)
        QuestionFewOptions.get_user_choice(options, options_check, user)

    @staticmethod
    def get_user_true_false(options, user):
        '''Логіка відповіді де або правильно або не правильно(True/False)'''

        QuestionTrueFalse.get_answers_for_question()
        QuestionTrueFalse.get_user_choice(options, user)

    @staticmethod
    def search_by_title(user_input):
        '''Пошук за назвою тесту'''

        return SearchTestByName.find_test(user_input)

    @staticmethod
    def search_by_description(user_input):
        '''Пошук за назвою тесту'''

        return SearchTestByDescription.find_test(user_input)
