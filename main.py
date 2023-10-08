from fixtures import LoadTests
from managers import TestManager, UserTestManager
from db import session, Test

'''Реалізувати систему перевірки знань, що підтримує 6-10 різних видів тестових питань
(введення відповіді, часткове співпадіння, вибір відповідей з переліку, шкала оцінки,
встановлення відповідностей та ін.). Надати можливість створювати сценарії тестів та
запускати процес проходження тестів на основі різних типів питань (передбачити
можливість, коли результати відповідей впливають складність та тематику наступних
питань). Створити кілька тестів та реалізувати процес проходження тестів на оцінку.
Додати режим адміністратора для створення та збереження тестів. Передбачити
обробку статистики по усім збереженим результатам окремого тесту (середній бал,
розподіл оцінок, найбільш складні питання тощо).'''


if __name__ == "__main__":
    LoadTests()

    while True:
        print('Оберіть тест:')
        for i, test in enumerate(TestManager.get_tests(), start=1):
            print(f"{test.id}. {test}")
        choice = int(input("Оберіть номер тесту: "))
        break

    test = session.query(Test).filter_by(id=choice).first()

    user = UserTestManager.start_test(1, test.id)
    if user:
        print(f"Начинаем тест '{test.name}'")
        for question in test.questions:
            print(f"Вопрос: {question.text}")
            UserTestManager.get_user_choice(
                [answer.text for answer in question.answers],
                [answer.is_correct for answer in question.answers],
                user)

        user = UserTestManager.finish_test(user.id)
        if user:
            print(f"Тест завершено. Ваш результат: {user.score}")
            print(f"Час початку: {user.start_time}")
            print(f"Час завершення: {user.end_time}")
            print(f"Загальний час проходження тесту {user.end_time - user.start_time}")
        else:
            print("Ошибка при завершении теста")
    else:
        print("Ошибка при начале теста")

    session.close()



