from fixtures import LoadTests
from managers import AdminTestManager, UserTestManager
from db import session, Test, TestsResults

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

    def main_menu(self):
        print('\t\tГоловне меню TestsQuiz')
        print('1. Пройти тест')
        print('2. Додати тест(Адмін)')
        print('3. Переглянути статистику успішності проходження тестів')
        choice = int(input("Оберіть варіант: "))
        return self.choices[choice-1]()

    @staticmethod
    def menu_test():
        while True:
            print('Оберіть тест:')
            for i, test in enumerate(AdminTestManager.get_tests(), start=1):
                print(f"{test.id}. {test}")
            choice = int(input("Оберіть номер тесту: "))
            break

        test = session.query(Test).filter_by(id=choice).first()

        user = UserTestManager.start_test(8, test.id)
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

                result = TestsResults(test.id, user, user.end_time - user.start_time, user.score)
                session.add(result)
                session.commit()
            else:
                print("Помилка при завершенні тесту")
        else:
            print("Помилка при початку тесту")

    @staticmethod
    def menu_add_test():
        pass

    @staticmethod
    def menu_check_stats():
        pass


if __name__ == "__main__":

    session.close()



