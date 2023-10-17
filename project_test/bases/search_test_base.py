from abc import ABC, abstractmethod

from project_test.db import session, Test


class SearchTestBase(ABC):

    @abstractmethod
    def find_test(self, user_input=None):
        pass


class SearchTestByName(SearchTestBase):
    '''Знайти тест за назвою тесту'''

    @staticmethod
    def find_test(user_input):
        found_tests = session.query(Test).filter(Test.name == user_input).all()

        return found_tests


class SearchTestByDescription(SearchTestBase):
    '''Знайти тест за описом тесту'''

    @staticmethod
    def find_test(user_input):
        found_tests = session.query(Test).filter(Test.description == user_input).all()

        return found_tests

