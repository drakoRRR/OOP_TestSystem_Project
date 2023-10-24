from datetime import datetime

from desgin_patterns.builder import TestBuilder, QuestionBuilder
from fixtures import LoadTests
from managers import AdminTestManager, UserTestManager
from db import session, Test, TestsResults

from desgin_patterns.Factory import QuestionFactory


class InterFace:
    def __init__(self):
        '''Ініцілізатор в якому завантажуємо усі створені тести та вибір меню'''

        LoadTests()
        self.__choices = [
            self.menu_test,
            self.menu_add_test,
            self.menu_del_test,
            self.menu_check_stats,
            self.menu_search_test
        ]

        self.__types = ['options_one_correct', 'options_few_correct', 'option_blank', 'option_bool']

    def main_menu(self):
        '''Меню користувача'''

        print('\t\tГоловне меню TestsQuiz')
        print('1. Пройти тест')
        print('2. Додати тест(Адмін)')
        print('3. Видалити тест(Адмін)')
        print('4. Переглянути статистику успішності проходження тестів')
        print('5. Знайти тест(Пошук)')
        choice = int(input("Оберіть варіант: "))
        return self.__choices[choice-1]()

    def menu_test(self, after_search=False, choice=None):
        '''Проходження тесту користувачем'''

        if not after_search:
            while True:
                print('Оберіть тест:')
                for i, test in enumerate(AdminTestManager.get_tests(), start=1):
                    print(f"{test.id}. {test}")
                choice = int(input("Оберіть номер тесту: "))
                break

        test = session.query(Test).filter_by(id=choice).first()

        user = UserTestManager.start_test(test.id)
        if user:
            print(f"Починаемо тест '{test.name}'")

            factory = QuestionFactory(questions=test.questions, user=user)
            questions = factory.get_list_of_questions()

            for question in questions:
                question()

            user = UserTestManager.finish_test(user.id)
            if user:
                print()
                print(f"Тест завершено. Ваш результат: {user.score}")
                print(f"Час початку: {user.start_time}")
                print(f"Час завершення: {user.end_time}")
                print(f"Загальний час проходження тесту {user.end_time - user.start_time}")

                result = TestsResults(test.id, user.id, datetime(1, 1, 1) + (user.end_time - user.start_time), user.score)

                session.add(result)
                session.commit()
            else:
                print("Помилка при завершенні тесту")
        else:
            print("Помилка при початку тесту")

    # def menu_add_test(self):
    #     '''Додавання тесту адміном'''
    #
    #     print('Яка кількість питань буде в тесті?')
    #     num_questions = int(input("Впишіть відповідь: "))
    #     test_data = []
    #
    #     for i in range(num_questions):
    #         print()
    #         print('1. Питання з одним правильним варіантом')
    #         print('2. Питання з декількома правильними варіантом')
    #         print('3. Питання з відкритою відповідь')
    #         print('4. Питання з на Правда/Не правда')
    #
    #         type_question = int(input("Оберіть тип питання: "))
    #         question_text = input(f"Впишіть текст питання {i + 1}: ")
    #         answer_options = []
    #
    #         num_options = int(input("Скільки варіантів відповідей для цього питання? "))
    #         for j in range(num_options):
    #             option_text = input(f"Впишіть текст варіанту відповіді {j + 1}: ")
    #             is_correct = input(f"Це правильна відповідь? (Так/Ні): ").strip().lower() == "так"
    #             answer_options.append((option_text, is_correct))
    #
    #         test_data.append((question_text, answer_options, self.__types[type_question-1]))
    #
    #     test_name = input("Впишіть назву тесту: ")
    #     test_description = input("Впишіть невеликий опис тесту: ")
    #     if not AdminTestManager.test_exists(test_name):
    #         test = AdminTestManager.create_test(test_name,
    #                                              test_description,
    #                                              test_data)
    #
    #         return test
    #
    #     return None

    def menu_add_test(self):
        '''Додавання тесту адміном'''

        print('Яка кількість питань буде в тесті?')
        num_questions = int(input("Впишіть відповідь: "))
        test_builder = TestBuilder()

        for i in range(num_questions):
            print()
            print('1. Питання з одним правильним варіантом')
            print('2. Питання з декількома правильними варіантом')
            print('3. Питання з відкритою відповідь')
            print('4. Питання з на Правда/Не правда')

            type_question = int(input("Оберіть тип питання: "))
            question_text = input(f"Впишіть текст питання {i + 1}: ")
            answer_options = []

            num_options = int(input("Скільки варіантів відповідей для цього питання? "))

            for j in range(num_options):
                option_text = input(f"Впишіть текст варіанту відповіді {j + 1}: ")
                is_correct = input(f"Це правильна відповідь? (Так/Ні): ").strip().lower() == "так"
                answer_options.append((option_text, is_correct))

            test_builder.add_question((question_text, answer_options, self.__types[type_question-1]))

        test_name = input("Впишіть назву тесту: ")
        test_description = input("Впишіть невеликий опис тесту: ")
        test = test_builder.set_name(test_name)
        test.test_description = test_description

        return test.build()

    @staticmethod
    def menu_check_stats():
        '''Зібрана уся статистика по тестам'''

        print(f"Статистика проходження усіх тестів які існують: ")
        print(f"середній балл проходження: {TestsResults.avg_score(session)}")
        print(f"середній час проходження: {TestsResults.avg_time(session)}")
        print()

        for i, test in enumerate(AdminTestManager.get_tests(), start=1):
            print(f"Статистика для тесту: {test.name}")
            try:
                print(f"середній балл проходження: {TestsResults.avg_score_for_test(session, test.id)}")
                print(f"середній час проходження: {TestsResults.avg_time_for_test(session, test.id)}")
            except TypeError:
                print(f"Для цього тесту ще немає статистики")

    @staticmethod
    def menu_del_test():
        while True:
            print('Оберіть тест який хочете видалити:')
            for i, test in enumerate(AdminTestManager.get_tests(), start=1):
                print(f"{test.id}. {test}")
            choice = int(input("Оберіть номер тесту: "))
            break

        AdminTestManager.delete_test(choice)
        return None

    def menu_search_test(self):
        print('За яким критерієм ви шукаете книгу ?')
        print('1. За назвою')
        print('2. За описом')
        choice_category = int(input('Ваша відповідь: '))

        user_search = input('Пошук: ')

        tests = UserTestManager.get_search(choice_category, user_search)

        print('Результати: ')

        for test in tests:
            print(f'{test.id}. {test.name}')

        test_to_pass = int(input('Який тест ви хочете пройти: '))

        return self.menu_test(after_search=True, choice=test_to_pass)
