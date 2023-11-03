# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
# from PyQt5.QtCore import QFile
#
# app = QApplication([])
# app.setStyle('Fusion')
#
#
# class Interface(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("TestsQuiz")
#         self.setGeometry(100, 100, 800, 600)
#
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
#
#         self.create_menu_buttons(layout)
#
#     def create_menu_buttons(self, layout):
#         menu_buttons = [
#             "Пройти тест",
#             "Додати тест (Адмін)",
#             "Видалити тест (Адмін)",
#             "Переглянути статистику успішності проходження тестів",
#             "Знайти тест (Пошук)",
#         ]
#
#         for text in menu_buttons:
#             button = QPushButton(text)
#             layout.addWidget(button)
#             # Применение стилей из файла CSS
#             button.setStyleSheet("QPushButton { font-size: 18px; }")
#             button.clicked.connect(self.handle_menu_button_click)
#
#     def handle_menu_button_click(self):
#         # Обработчик нажатия кнопок меню
#         sender = self.sender()
#         if sender:
#             button_text = sender.text()
#             if button_text == "Пройти тест":
#                 # Добавьте код для просмотра списка тестов и начала прохождения
#                 pass
#             elif button_text == "Додати тест (Адмін)":
#                 # Добавьте код для добавления нового теста
#                 pass
#             elif button_text == "Видалити тест (Адмін)":
#                 # Добавьте код для удаления теста
#                 pass
#             elif button_text == "Переглянути статистику успішності проходження тестів":
#                 # Добавьте код для просмотра статистики
#                 pass
#             elif button_text == "Знайти тест (Пошук)":
#                 # Добавьте код для поиска теста
#                 pass
#
#
# if __name__ == "__main__":
#     window = Interface()
#     window.show()
#
#     # Загрузка стилей из файла CSS
#     style_file = QFile("static/styles_interface.css")
#     print(style_file.readAll())
#     if style_file.open(QFile.ReadOnly | QFile.Text):
#         style_sheet = style_file.readAll().data().decode("utf-8")
#         app.setStyleSheet(style_sheet)
#         style_file.close()
#
#     app.exec_()