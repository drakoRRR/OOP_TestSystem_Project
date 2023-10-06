from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, JSON, select

meta = MetaData()

engine = create_engine('postgresql+psycopg2://youuser:youpassword@localhost/youdb')
class DatabaseTests:
    def __init__(self):
        self.tests = Table('Tests', meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('test_title', String(250), nullable=False),
            Column('test', JSON, nullable=False),
            Column('complexity', Integer, nullable=False)
        )
        self.conn = engine.connect()

    def add_test(self, test_title: str, test, complexity: int):
        test = self.tests.insert().values(
            test_title=test_title,
            test=test,
            complexity=complexity
        )

        return self.conn.execute(test)

    def delete_test(self, title):
        try:
            delete_query = self.tests.delete().where(self.tests.c.test_title == title)
            result = self.conn.execute(delete_query)
            return result
        except Exception as e:
            print(f"Error deleting test: {e}")
            return None

    def get_test_by_title(self, title: str):
        select_query = select([self.tests]).where(self.tests.c.test_title == title)
        self.conn.execute(select_query)
        return select_query


class DatabaseQuestion:
    pass


class DatabaseUser:
    pass
