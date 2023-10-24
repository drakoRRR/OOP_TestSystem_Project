from project_test.bases.question_base import QuestionOptions, QuestionFewOptions, QuestionUserBlank, QuestionTrueFalse


class QuestionFactory:
    def __init__(self, questions, search=None, user=None):
        self.questions = questions
        self.search = search
        self.user = user

        self.type_of_questions = {
            'options_one_correct': QuestionOptions,
            'options_few_correct': QuestionFewOptions,
            'option_blank': QuestionUserBlank,
            'option_bool': QuestionTrueFalse
        }

    def get_list_of_questions(self):
        list_of_questions = []

        for question in self.questions:
            question_text = question.text
            type_of_question = question.types.type_question
            options = [answer.text for answer in question.answers]
            options_check = [answer.is_correct for answer in question.answers]

            object_class = self.type_of_questions[type_of_question](options, options_check, self.user, question_text)

            list_of_questions.append(object_class)

        return list_of_questions


