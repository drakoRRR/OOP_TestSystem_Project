from managers import AdminTestManager
from project_test.db import Types, session


class LoadTests:
    def __init__(self):
        '''Створені тести які потім завантажуємо для користувачів'''
        self.types = ['options_one_correct', 'options_few_correct', 'option_blank', 'option_bool']

        for type_text in self.types:
            if not Types.exists(type_text):
                type_add = Types(type_question=type_text)
                session.add(type_add)

        session.commit()

        test_data1 = [
            ("Яка столиця України?", [("Київ", True), ("Львів", False), ("Одеса", False)], 'options_one_correct'),
            ("Скільки областей в Україні?", [("24", True), ("25", False), ("23", False)], 'options_one_correct'),
            ("Яка найвища гора в Україні?", [("Говерла", True), ("Піп Іван", False), ("Петрос", False)],
             'options_one_correct'),
            ("Хто є автором гімну України?",
             [("Павло Чубинський", True), ("Тарас Шевченко", False), ("Іван Франко", False)], 'options_one_correct'),
            ("В якому році була проголошена незалежність України?", [("1991", True), ("1992", False), ("1990", False)],
             'options_one_correct'),
            ("Яка найбільша річка в Україні?", [("Дніпро", True), ("Дунай", False), ("Південний Буг", False)],
             'options_one_correct'),
            ("Яке море омиває Україну?", [("Чорне", True), ("Азовське", False), ("Балтійське", False)],
             'options_one_correct')
        ]

        test_data2 = [
            ("Хто є автором 'Кобзаря'?", [("Тарас Шевченко", True), ("Іван Франко", False), ("Леся Українка", False)],
             'options_one_correct'),
            ("В якому році народився Тарас Шевченко?", [("1814", True), ("1815", False), ("1813", False)],
             'options_one_correct'),
            ("Де народився Тарас Шевченко?", [("Моринці", True), ("Київ", False), ("Харків", False)],
             'options_one_correct'),
            ("Як називається перше видання 'Кобзаря'?",
             [("Перший 'Кобзар'", True), ("'Кобзар' 1840", False), ("'Кобзар' Шевченка", False)],
             'options_one_correct'),
            ("В якому році помер Тарас Шевченко?", [("1861", True), ("1860", False), ("1862", False)],
             'options_one_correct'),
            ("Де похований Тарас Шевченко?",
             [("Чернеча гора", True), ("Байкове кладовище", False), ("Лук'янівське кладовище", False)],
             'options_one_correct'),
            ("Хто є автором поеми 'Гайдамаки'?",
             [("Тарас Шевченко", True), ("Іван Франко", False), ("Леся Українка", False)], 'options_one_correct')
        ]

        test_data3 = [
            ("Хто є автором 'Захар Беркут'?",
             [("Іван Франко", True), ("Тарас Шевченко", False), ("Леся Українка", False)], 'options_one_correct'),
            ("В якому році народився Іван Франко?", [("1856", True), ("1857", False), ("1855", False)],
             'options_one_correct'),
            ("Де народився Іван Франко?", [("Нагуєвичі", True), ("Львів", False), ("Івано-Франківськ", False)],
             'options_one_correct'),
            ("Як називається перше видання 'Захар Беркут'?",
             [("Перший 'Захар Беркут'", True), ("'Захар Беркут' 1883", False), ("'Захар Беркут' Франка", False)],
             'options_one_correct'),
            ("В якому році помер Іван Франко?", [("1916", True), ("1915", False), ("1917", False)],
             'options_one_correct'),
            ("Де похований Іван Франко?",
             [("Личаківське кладовище", True), ("Байкове кладовище", False), ("Сахарна гора", False)],
             'options_one_correct'),
            ("Хто є автором поеми 'Мойсей'?",
             [("Іван Франко", True), ("Тарас Шевченко", False), ("Леся Українка", False)], 'options_one_correct')
        ]

        test_data4 = [
            ("Хто був першим Гетьманом України?",
             [("Богдан Хмельницький", True), ("Іван Мазепа", False), ("Петро Сагайдачний", False)],
             'options_one_correct'),
            ("В якому році відбулася Битва під Полтавою?", [("1709", True)], 'option_blank'),
            ("Де відбулась Битва під Полтавою?", [("Полтава", True)], 'option_blank'),
            ("Як називається угода, яка поклала кінець війні між Річчю Посполитою та Османською імперією в 1683 році?",
             [("Карловицький мир", True), ("Берестейська унія", False), ("Андріївська угода", False)],
             'options_one_correct'),
            ("В якому році відбулась Чигиринська кампанія?", [("1678", True)], 'option_blank'),
            ("Де знаходиться Чорнобильська АЕС?", [("Прип'ять", True), ("Чернігів", False), ("Київ", False)],
             'options_one_correct'),
            ("Хто був першим президентом України?", [("Леонід Кравчук", True)], 'option_blank')
        ]

        test_data5 = [
            ("Чи є Київ столицею України?", [("Так", True), ("Ні", False)], 'option_bool'),
            ("Чи є 24 області в Україні?", [("Так", True), ("Ні", False)], 'option_bool'),
            ("Чи є Говерла найвищою горою в Україні?", [("Так", True), ("Ні", False)], 'option_bool'),
            ("Чи є Павло Чубинський автором гімну України?", [("Так", True), ("Ні", False)], 'option_bool'),
            ("Чи була незалежність України проголошена в 1991 році?", [("Так", True), ("Ні", False)], 'option_bool'),
            ("Чи є Дніпро найбільшою річкою в Україні?", [("Так", True), ("Ні", False)], 'option_bool'),
            ("Чи омиває Чорне море Україну?", [("Так", True), ("Ні", False)], 'option_bool')
        ]

        test_name = "Загальні знання про Україну"
        if not AdminTestManager.test_exists(test_name):
            test1 = AdminTestManager.create_test(test_name, "Тест на знання загальних фактів про Україну", test_data1)

        test_name = "Тарас Шевченко"
        if not AdminTestManager.test_exists(test_name):
            test2 = AdminTestManager.create_test(test_name,
                                                 "Тест на знання фактів з життя та творчості Тараса Шевченка",
                                                 test_data2)

        test_name = "Іван Франко"
        if not AdminTestManager.test_exists(test_name):
            test3 = AdminTestManager.create_test(test_name, "Тест на знання фактів з життя та творчості Івана Франка",
                                                 test_data3)

        test_name = "Історія України"
        if not AdminTestManager.test_exists(test_name):
            test4 = AdminTestManager.create_test(test_name, "Тест на знання фактів з історії України", test_data4)

        test_name = "Базові знання"
        if not AdminTestManager.test_exists(test_name):
            test5 = AdminTestManager.create_test(test_name, "Тест на базові знання", test_data5)
