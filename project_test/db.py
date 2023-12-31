import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Time, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from dotenv import load_dotenv

import os


load_dotenv()
engine = create_engine('postgresql+psycopg2://{}:{}@localhost/{}'.format(os.getenv('USER_DB'),
                                                                         os.getenv('PASSWORD_DB'),
                                                                         os.getenv('NAME_DB'),))
Base = declarative_base()


class Test(Base):
    '''Модель для збереження тестів'''

    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    questions = relationship('Question', back_populates='test')

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Types(Base):
    '''Типи питань'''

    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_question = Column(String)

    questions = relationship('Question', back_populates='types')

    def __str__(self):
        return self.type_question

    @staticmethod
    def exists(type_question_pr):
        return True if session.query(Types).filter_by(type_question=type_question_pr).first() else False

class Question(Base):
    '''Модель збереження питань для тесту'''

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    test_id = Column(Integer, ForeignKey('tests.id'))
    type_id = Column(Integer, ForeignKey('types.id'))

    test = relationship('Test', back_populates='questions')
    answers = relationship('Answer', back_populates='question')
    types = relationship('Types', back_populates='questions')

    def __init__(self, text, test_id, type_id):
        self.text = text
        self.test_id = test_id
        self.type_id = type_id

    def __str__(self):
        return self.text

class Answer(Base):
    '''Модель збереження відповідей до питань'''

    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship('Question', back_populates='answers')

    def __init__(self, text, is_correct, question_id):
        self.text = text
        self.is_correct = is_correct
        self.question_id = question_id

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'Answer: {self.text}, is_correct: {self.is_correct}'

class User(Base):
    '''Модель для збереження користувачів тесту'''

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    score = Column(Integer, default=0)

    def __init__(self, test_id, start_time, end_time=None, score=None):
        self.test_id = test_id
        self.start_time = start_time
        self.end_time = end_time
        self.score = score

    def __str__(self):
        return self.id


class TestsResults(Base):
    '''Модель збереження статистики по пройденими тестам'''

    __tablename__ = 'tests_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    user = Column(Integer, ForeignKey('users.id'))
    time_complete = Column(Time)  #Time
    score = Column(Integer)

    def __init__(self, test_id, user, time_complete, score):
        self.test_id = test_id
        self.user = user
        self.time_complete = time_complete
        self.score = score

    def __str__(self):
        return f'User: {self.user.id}, test: {self.test_id}, score: {self.score}'

    @staticmethod
    def avg_score(session):
        '''Середній балл користувачів усіх тестів'''

        avg_score = session.query(func.avg(TestsResults.score)).scalar()
        return round(avg_score, 2)

    @staticmethod
    def avg_score_for_test(session, test_id):
        '''Середній балл користувачів окремого тесту'''

        avg_score = session.query(func.avg(TestsResults.score)).filter_by(test_id=test_id).scalar()
        return round(avg_score, 2)

    @staticmethod
    def avg_time(session):
        '''Середній час проходження користувачів усіх тестів'''

        avg_time_seconds = session.query(func.avg(func.extract('epoch', TestsResults.time_complete))).scalar()
        avg_time = datetime.timedelta(seconds=int(avg_time_seconds))
        return avg_time

    @staticmethod
    def avg_time_for_test(session, test_id):
        '''Середній час проходження користувачів окремого тесту'''

        avg_time_seconds = session.query(func.avg(func.extract('epoch', TestsResults.time_complete))).filter_by(
            test_id=test_id).scalar()
        avg_time = datetime.timedelta(seconds=int(avg_time_seconds))
        return avg_time


# Під'єднання до БД та створення сесії
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

