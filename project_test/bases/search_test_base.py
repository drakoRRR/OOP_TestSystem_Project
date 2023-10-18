from abc import ABC, abstractmethod

from project_test.db import session, Test


class SearchTestBase(ABC):
    @abstractmethod
    def find_test(self):
        pass


class SearchTestByName(SearchTestBase):
    '''Знайти тест за назвою тесту'''

    def __init__(self, user_input):
        self.user_input = user_input

    def find_test(self):
        found_tests = session.query(Test).filter(Test.name == self.user_input).all()

        return found_tests


class SearchTestByDescription(SearchTestBase):
    '''Знайти тест за описом тесту'''

    def __init__(self, user_input):
        self.user_input = user_input

    def find_test(self):
        found_tests = session.query(Test).filter(Test.description == self.user_input).all()

        return found_tests

