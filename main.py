from datetime import datetime

from fixtures import LoadTests
from managers import AdminTestManager, UserTestManager
from db import session, Test, TestsResults
from sqlalchemy import cast, Interval

'''Реалізувати систему перевірки знань, що підтримує 6-10 різних видів тестових питань
(введення відповіді, часткове співпадіння, вибір відповідей з переліку, шкала оцінки,
встановлення відповідностей та ін.). Надати можливість створювати сценарії тестів та
запускати процес проходження тестів на основі різних типів питань (передбачити
можливість, коли результати відповідей впливають складність та тематику наступних
питань). Створити кілька тестів та реалізувати процес проходження тестів на оцінку.
Додати режим адміністратора для створення та збереження тестів. Передбачити
обробку статистики по усім збереженим результатам окремого тесту (середній бал,
розподіл оцінок, найбільш складні питання тощо).'''

class InterFace:
    def __init__(self):
        LoadTests()
        self.choices = [self.menu_test, self.menu_add_test, self.menu_check_stats]
        self.user_id = 16

    def main_menu(self):
        print('\t\tГоловне меню TestsQuiz')
        print('1. Пройти тест')
        print('2. Додати тест(Адмін)')
        print('3. Переглянути статистику успішності проходження тестів')
        choice = int(input("Оберіть варіант: "))
        return self.choices[choice-1]()

    def menu_test(self):
        while True:
            print('Оберіть тест:')
            for i, test in enumerate(AdminTestManager.get_tests(), start=1):
                print(f"{test.id}. {test}")
            choice = int(input("Оберіть номер тесту: "))
            break

        test = session.query(Test).filter_by(id=choice).first()

        user = UserTestManager.start_test(self.user_id, test.id)
        if user:
            print(f"Починаемо тест '{test.name}'")
            for question in test.questions:
                print(f"Питання: {question.text}\n")
                if len(question.answers) > 1:
                    UserTestManager.get_user_choice_by_options(
                        [answer.text for answer in question.answers],
                        [answer.is_correct for answer in question.answers],
                        user)
                else:
                    UserTestManager.get_user_choice(option_check=[answer.text for answer in question.answers],
                                                    user=user)

            user = UserTestManager.finish_test(user.id)
            if user:
                print()
                print(f"Тест завершено. Ваш результат: {user.score}")
                print(f"Час початку: {user.start_time}")
                print(f"Час завершення: {user.end_time}")
                print(f"Загальний час проходження тесту {user.end_time - user.start_time}")

                result = TestsResults(test.id, self.user_id, datetime(1, 1, 1) + (user.end_time - user.start_time), user.score)
                session.add(result)
                session.commit()
            else:
                print("Помилка при завершенні тесту")
        else:
            print("Помилка при початку тесту")

    @staticmethod
    def menu_add_test():
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
        print(f"Статистика проходження усіх тестів які існують: ")
        print(f"середній балл проходження: {TestsResults.avg_score(session)}")
        print(f"середній час проходження: {TestsResults.avg_time(session)}")
        print()

        for i, test in enumerate(AdminTestManager.get_tests(), start=1):
            print(f"Статистика для тесту: {test.name}")
            print(f"середній балл проходження: {TestsResults.avg_score_for_test(session, test.id)}")
            print(f"середній час проходження: {TestsResults.avg_time_for_test(session, test.id)}")


if __name__ == "__main__":
    menu = InterFace()
    menu.main_menu()

    session.close()



