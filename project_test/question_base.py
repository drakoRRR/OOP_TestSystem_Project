from abc import abstractmethod, ABC

class QuestionBase(ABC):
    @abstractmethod
    def get_question(self):
        '''Отримати тест для подальшої відповіді користувача'''

        pass

    @abstractmethod
    def get_user_choice(self):
        '''Отримати відповідь для подальшої відповіді користувача'''

        pass


class QuestionOptions(QuestionBase):
    '''Відповідь на питання де тільки одна відповідь правильна з наданих'''

    def get_question(self):
        pass

    def get_user_choice(self):
        pass


class QuestionUserBlank(QuestionBase):
    '''Відповідь вписує користувач'''

    def get_question(self):
        pass

    def get_user_choice(self):
        pass


class QuestionFewOptions(QuestionBase):
    '''Відповідь на питання де декілька варіантів правильні з наданих'''

    def get_question(self):
        pass

    def get_user_choice(self):
        pass