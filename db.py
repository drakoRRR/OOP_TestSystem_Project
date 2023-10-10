import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, func, Interval
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from dotenv import load_dotenv

import os


load_dotenv()
engine = create_engine('postgresql+psycopg2://{}:{}@localhost/{}'.format(os.getenv('USER_DB'),
                                                                         os.getenv('PASSWORD_DB'),
                                                                         os.getenv('NAME_DB'),))
Base = declarative_base()


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    questions = relationship('Question', back_populates='test')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    test_id = Column(Integer, ForeignKey('tests.id'))

    test = relationship('Test', back_populates='questions')
    answers = relationship('Answer', back_populates='question')

    def __init__(self, text, test_id):
        self.text = text
        self.test_id = test_id

    def __str__(self):
        return self.text

class Answer(Base):
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
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    score = Column(Integer, default=0)

    def __init__(self, id, test_id, start_time, end_time=None, score=None):
        self.id = id
        self.test_id = test_id
        self.start_time = start_time
        self.end_time = end_time
        self.score = score

    def __str__(self):
        return self.id


class TestsResults(Base):
    __tablename__ = 'tests_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    user = Column(Integer, ForeignKey('users.id'))
    time_complete = Column(DateTime)
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
        avg_score = session.query(func.avg(TestsResults.score)).scalar()
        return round(avg_score)

    @staticmethod
    def avg_score_for_test(session, test_id):
        avg_score = session.query(func.avg(TestsResults.score)).filter_by(test_id=test_id).scalar()
        return round(avg_score)

    @staticmethod
    def avg_time(session):
        avg_time_seconds = session.query(func.avg(func.extract('epoch', TestsResults.time_complete))).scalar()
        avg_time = datetime.datetime.fromtimestamp(avg_time_seconds)
        return avg_time

    @staticmethod
    def avg_time_for_test(session, test_id):
        avg_time_seconds = session.query(func.avg(func.extract('epoch', TestsResults.time_complete))).filter_by(
            test_id=test_id).scalar()
        avg_time = datetime.datetime.fromtimestamp(avg_time_seconds)
        return avg_time


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

