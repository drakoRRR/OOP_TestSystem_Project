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


class QuestionOptions(QuestionBase):
    '''Відповідь на питання де тільки одна відповідь правильна з наданих'''

    @staticmethod
    def get_answers_for_question(options):
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

    @staticmethod
    def get_user_choice(options, options_check, user):
        while True:
            try:
                choice = int(input("Оберіть номер відповіді: "))
                if 1 <= choice <= len(options):
                    if options_check[choice - 1]:
                        user.score += 1
                        session.commit()
                    return choice
                else:
                    print("Будь ласка, оберіть правильный номер.")
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")


class QuestionUserBlank(QuestionBase):
    '''Відповідь вписує користувач'''

    def get_answers_for_question(self):
        pass

    @staticmethod
    def get_user_choice(option_check, user):
        while True:
            try:
                choice = input("Напишіть відповідь: ")
                # Перевести у
                if option_check[0].lower() == choice.lower():
                    user.score += 1
                    session.commit()
                    return choice
                else:
                    return choice
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")


class QuestionFewOptions(QuestionBase):
    '''Відповідь на питання де декілька варіантів правильні з наданих'''

    @staticmethod
    def get_answers_for_question(options):
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

    @staticmethod
    def get_user_choice(options, options_check, user):
        correct_percent = 0

        while True:
            try:
                choices = map(int, input("Оберіть номери відповіді через пробіл: ").split())
                for choice in choices:
                    if 1 <= choice <= len(options):
                        if options_check[choice - 1]:
                            correct_percent += 0.25
                    else:
                        print("Будь ласка, оберіть правильный номер.")

                user.score += correct_percent
                session.commit()

                return None
            except ValueError:
                print("Будь ласка, введіть номер відповіді.")


class QuestionTrueFalse(QuestionBase):
    '''Відповідь на вопросы типа "Правда" або "Брехня"'''

    @staticmethod
    def get_answers_for_question():
        pass

    @staticmethod
    def get_user_choice(options, user):
        while True:
            try:
                choice = input("Впишіть так або ні: ")
                right_answer = None

                for option in options:
                    if option.is_correct:
                        right_answer = option.text

                if right_answer.lower() == choice.lower():
                    user.score += 1
                    session.commit()
                    return choice

                return None

            except ValueError:
                print("Будь ласка, впишіть так або ні.")

