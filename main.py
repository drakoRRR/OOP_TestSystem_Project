from typing import List


class Question:
    '''Представляє окреме питання в тесті з можливими відповідями.'''

    def __init__(self, question_text: str, answers: list):
        self.question_text = question_text
        self.answers = answers

    def add_answer(self, answer):
        '''Додавання відповіді до питання.'''
        pass

    def remove_answer(self, answer):
        '''Видалення відповіді з питання.'''
        pass

    def get_answers(self):  # Возможно сделать геттером через свойство @property
        '''Отримання списку відповідей на питання.'''
        pass

    def set_correct_answer(self, index):  # Возможно сделать геттером через свойство @property
        pass

    def get_correct_answer(self):  # idk if we need it
        '''Отримання індексу вірної відповіді.'''
        pass

    def get_question_text(self):
        '''Отримання тексту питання.'''
        pass


class Test:
    '''Представляє тест з питаннями та відповідями.'''

    def __init__(self, test_name: str, questions: List[Question], difficulty: str):
        self.test_name = test_name
        self.questions = questions
        self.difficulty = difficulty

    def add_question(self, question):
        '''Додавання питання до тесту.'''
        pass

    def remove_question(self, question):
        '''Видалення питання з тесту.'''
        pass

    def get_questions(self):  # Возможно сделать геттером через свойство @property
        '''Отримання списку питань тесту.'''
        pass

    def set_difficulty(self, difficulty):  # Возможно сделать геттером через свойство @property
        '''Встановлення рівня складності тесту.'''
        pass

    def get_difficulty(self):  # Возможно сделать геттером через свойство @property
        '''Отримання рівня складності тесту.'''
        pass

    def get_test_name(self):  # Возможно сделать геттером через свойство @property
        '''Отримання назви тесту.'''
        pass


class TestResult:
    '''Представляє результат проходження тесту.'''

    def __init__(self, test, user, score):
        self.__test = test
        self.__user = user
        self.__score = score

    @property
    def test(self):
        return self.__test

    @property
    def user(self):
        return self.__user

    @property
    def score(self):
        return self.__score


class User:
    '''Представляє користувача системи.'''

    def __init__(self, username: str, email :str, test_results: TestResult):
        self.username = username
        self.email = email
        self.test_results = test_results

    def take_test(self, test):
        ''' Проходження тесту та збереження результату.'''
        pass

    def get_test_results(self):  # Возможно сделать геттером через свойство @property
        '''Отримання списку результатів тестів користувача.'''
        pass

    def get_username(self):  # Возможно сделать геттером через свойство @property
        '''Отримання імені користувача.'''
        pass

    def get_email(self):  # Возможно сделать геттером через свойство @property
        '''Отримання адреси електронної пошти користувача.'''
        pass


class Manager:
    '''Клас фасад'''

    def __init__(self):
        pass

class Interface:
    pass