from datetime import datetime

from fixtures import LoadTests
from managers import AdminTestManager, UserTestManager
from db import session, Test, TestsResults

from bases.question_base import QuestionOptions, QuestionFewOptions, QuestionTrueFalse, QuestionUserBlank

class InterFace:
    def __init__(self):
        '''Ініцілізатор в якому завантажуємо усі створені тести та вибір меню'''

        LoadTests()
        self.choices = [
            self.menu_test,
            self.menu_add_test,
            self.menu_del_test,
            self.menu_check_stats,
            self.menu_search_test
        ]

        self.types = ['options_one_correct', 'options_few_correct', 'option_blank', 'option_bool']

    def main_menu(self):
        '''Меню користувача'''

        print('\t\tГоловне меню TestsQuiz')
        print('1. Пройти тест')
        print('2. Додати тест(Адмін)')
        print('3. Видалити тест(Адмін)')
        print('4. Переглянути статистику успішності проходження тестів')
        print('5. Знайти тест(Пошук)')
        choice = int(input("Оберіть варіант: "))
        return self.choices[choice-1]()

    @staticmethod
    def menu_test(after_search=False, choice=None):
        '''Проходження тесту користувачем'''

        if not after_search:
            while True:
                print('Оберіть тест:')
                for i, test in enumerate(AdminTestManager.get_tests(), start=1):
                    print(f"{test.id}. {test}")
                choice = int(input("Оберіть номер тесту: "))
                break

        types = ['options_one_correct', 'options_few_correct', 'option_blank', 'option_bool']
        test = session.query(Test).filter_by(id=choice).first()

        user = UserTestManager.start_test(test.id)
        if user:
            print(f"Починаемо тест '{test.name}'")
            for question in test.questions:
                print(f"Питання: {question.text}\n")
                if question.types.type_question == types[0]:
                    UserTestManager.get_user_choice_by_options(
                        [answer.text for answer in question.answers],
                        [answer.is_correct for answer in question.answers],
                        user)
                elif question.types.type_question == types[1]:
                    UserTestManager.get_user_few_choices(
                        [answer.text for answer in question.answers],
                        [answer.is_correct for answer in question.answers],
                        user)
                elif question.types.type_question == types[2]:
                    UserTestManager.get_user_choice(option_check=[answer.text for answer in question.answers],
                                                    user=user)
                elif question.types.type_question == types[3]:
                    UserTestManager.get_user_true_false(
                        [answer for answer in question.answers],
                        user)

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

    @staticmethod
    def menu_add_test():
        '''Додавання тесту адміном'''

        print('Яка кількість питань буде в тесті?')
        num_questions = int(input("Впишіть відповідь: "))
        test_data = []

        for i in range(num_questions):
            question_text = input(f"Впишіть текст питання {i + 1}: ")
            answer_options = []

            num_options = int(input("Скільки варіантів відповідей для цього питання? "))
            for j in range(num_options):
                option_text = input(f"Впишіть текст варіанту відповіді {j + 1}: ")
                is_correct = input(f"Це правильна відповідь? (Так/Ні): ").strip().lower() == "так"
                answer_options.append((option_text, is_correct))

            test_data.append((question_text, answer_options))

        test_name = input("Впишіть назву тесту: ")
        test_description = input("Впишіть невеликий опис тесту: ")
        if not AdminTestManager.test_exists(test_name):
            test = AdminTestManager.create_test(test_name,
                                                 test_description,
                                                 test_data)

            return test

        return None

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

        if choice_category == 1:
            tests = UserTestManager.search_by_title(user_search)
        else:
            tests = UserTestManager.search_by_description(user_search)

        print('Результати: ')

        for test in tests:
            print(f'{test.id}. {test.name}')

        test_to_pass = int(input('Який тест ви хочете пройти: '))

        return self.menu_test(after_search=True, choice=test_to_pass)
