from project_test.managers import AdminTestManager


class TestBuilder:
    def __init__(self):
        self.test_name = None
        self.test_description = None
        self.test_questions = []

    def set_name(self, name):
        self.test_name = name
        return self

    def set_description(self, description):
        self.test_description = description
        return self

    def add_question(self, question):
        self.test_questions.append(question)
        return self

    def build(self):
        test = AdminTestManager.create_test(self.test_name,
                                            self.test_description,
                                            self.test_questions)

        return test
