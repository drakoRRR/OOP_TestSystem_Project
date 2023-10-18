from abc import abstractmethod, ABC

from project_test.db import session


class QuestionBase(ABC):

    @abstractmethod
    def get_answers_for_question(self):
        '''Отримати тест для подальшої відповіді користувача'''

        pass

    @abstractmethod
    def get_user_choice(self):
        '''Отримати відповідь для подальшої відповіді користувача'''

        pass

    @abstractmethod
    def get_question(self):
        '''Отримати питання'''

        pass

    def __call__(self):
        self.get_question()
        self.get_answers_for_question()
        self.get_user_choice()


class QuestionOptions(QuestionBase):
    '''Відповідь на питання де тільки одна відповідь правильна з наданих'''

    def __init__(self, options, options_check, user, question_text):
        self.options = options
        self.options_check = options_check
        self.user = user
        self.question_text = question_text

    def get_question(self):
        print(f"Питання: {self.question_text}\n")

    def get_answers_for_question(self):
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")

    def get_user_choice(self):
        while True:
            try:
                choice = int(input("Оберіть номер відповіді: "))
                if 1 <= choice <= len(self.options):
                    if self.options_check[choice - 1]:
                        self.user.score += 1
                        session.commit()
                    return choice
                else:
                    print("Будь ласка, оберіть правильный номер.")
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")


class QuestionUserBlank(QuestionBase):
    '''Відповідь вписує користувач'''

    def __init__(self, options, options_check, user, question_text):
        self.options = options
        self.options_check = options_check
        self.user = user
        self.question_text = question_text

    def get_question(self):
        print(f"Питання: {self.question_text}\n")

    def get_answers_for_question(self):
        pass

    def get_user_choice(self):
        while True:
            try:
                choice = input("Напишіть відповідь: ")
                if self.options[0].lower() == choice.lower():
                    self.user.score += 1
                    session.commit()
                    return choice
                else:
                    return choice
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")


class QuestionFewOptions(QuestionBase):
    '''Відповідь на питання де декілька варіантів правильні з наданих'''

    def __init__(self, options, options_check, user, question_text):
        self.options = options
        self.options_check = options_check
        self.user = user
        self.question_text = question_text

    def get_question(self):
        print(f"Питання: {self.question_text}\n")

    def get_answers_for_question(self):
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")

    def get_user_choice(self):
        correct_percent = 0

        while True:
            try:
                choices = map(int, input("Оберіть номери відповіді через пробіл: ").split())
                for choice in choices:
                    if 1 <= choice <= len(self.options):
                        if self.options_check[choice - 1]:
                            correct_percent += 0.25
                    else:
                        print("Будь ласка, оберіть правильный номер.")

                self.user.score += correct_percent
                session.commit()

                return None
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")


class QuestionTrueFalse(QuestionBase):
    '''Відповідь на питання типу "Правда" або "Брехня"'''

    def __init__(self, options, options_check, user, question_text):
        self.options = options
        self.options_check = options_check
        self.user = user
        self.question_text = question_text

    def get_question(self):
        print(f"Питання: {self.question_text}\n")

    def get_answers_for_question(self):
        pass

    def get_user_choice(self):
        while True:
            try:
                choice = input("Впишіть так або ні: ")
                right_answer = self.options[self.options_check.index(True)]

                if right_answer.lower() == choice.lower():
                    self.user.score += 1
                    session.commit()
                    return choice

                return None

            except ValueError:
                print("Будь ласка, впишіть так або ні.")

