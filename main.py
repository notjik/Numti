# Импортирование библиотек (Importing libraries)
import sys
import json

from data import checknum
from dsgn import design
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem


# Создание главного окна (Creating the main window)
class Window(QMainWindow, design.Ui_MainWindow):
    # Инициализирование дизайна (Design Initialization)
    def __init__(self):
        super(Window, self).__init__()
        # uic.loadUi("dsgn/design.ui", self)
        self.setupUi(self)
        QApplication.setApplicationName(f"Numti")
        QApplication.setApplicationVersion(self.config['version'])
        QApplication.setApplicationDisplayName(f"Numti v{self.config['version']}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("numti_logx.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QApplication.setWindowIcon(icon)
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap(f"dsgn/eye-{self.config['theme']}.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon11 = QtGui.QIcon()
        self.icon11.addPixmap(QtGui.QPixmap(f"dsgn/eyeslash-{self.config['theme']}.ico"), QtGui.QIcon.Normal,
                              QtGui.QIcon.Off)
        self.pushButton.clicked.connect(self.run)
        self.pushButton1.clicked.connect(self.addcontact)
        self.pushButton2.clicked.connect(self.editcontact)
        self.pushButton3.clicked.connect(self.deletecontact)
        self.comboBox.currentIndexChanged.connect(self.change)
        self.actionAbout_programm.triggered.connect(self.aboutprogramm)
        self.actionHow_to_use_the_program.triggered.connect(self.howtousetheprogram)
        self.settings()
        self.change()
        self.toolButton.clicked.connect(self.changedoc)
        if self.config['nh']:
            self.menubar.hide()
            self.closed.clicked.connect(self.close)
            self.seemenu.clicked.connect(self.changemenubar)
            self.roll.clicked.connect(self.showMinimized)
        self.lineEdit.textChanged.connect(self.edit_text)
        self.namedoc = ''

    def restart(self):
        self.hide()
        self.__init__()
        self.show()

    def edit_text(self):
        if self.comboBox.currentIndex() == 0:
            check = checknum.my_contact(self.lineEdit.text(), self.config['language'], self.config['translating'])
            if check and check != 499:
                for i, elem in enumerate(check):
                    self.tableWidget.setRowCount(i + 1)
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(elem[1]))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(elem[2]))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(elem[3]))
            elif check == 499:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "No connection.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Нет соединения.", QMessageBox.Ok)
            else:
                self.tableWidget.setRowCount(0)

    def changemenubar(self):
        if self.menubar.height():
            self.menubar.hide()
            self.setMinimumSize(QtCore.QSize(800, 590))
            self.setMaximumSize(QtCore.QSize(800, 590))
            self.seemenu.setIcon(self.icon1)
        else:
            self.menubar.show()
            self.setMinimumSize(QtCore.QSize(800, 610))
            self.setMaximumSize(QtCore.QSize(800, 610))
            self.seemenu.setIcon(self.icon11)

    def settings(self):
        self.Light.triggered.connect(self.light)
        self.Dark.triggered.connect(self.dark)
        self.Russian.triggered.connect(self.russian)
        self.English.triggered.connect(self.english)
        self.Translating.triggered.connect(self.translate)

    def translate(self):
        if self.Translating.isChecked():
            self.Translating.setChecked(True)
            self.config['translating'] = True
        else:
            self.Translating.setChecked(False)
            self.config['translating'] = False
        with open("data/numti.cfg", "w") as file:
            json.dump(self.config, file)
        self.restart()

    def light(self):
        self.Light.setChecked(True)
        self.Dark.setChecked(False)
        self.config['theme'] = 'light'
        with open("data/numti.cfg", "w") as file:
            json.dump(self.config, file)
        self.restart()

    def dark(self):
        self.Dark.setChecked(True)
        self.Light.setChecked(False)
        self.config['theme'] = 'dark'
        with open("data/numti.cfg", "w") as file:
            json.dump(self.config, file)
        self.restart()

    def russian(self):
        self.Russian.setChecked(True)
        self.English.setChecked(False)
        self.config['language'] = 'ru'
        with open("data/numti.cfg", "w") as file:
            json.dump(self.config, file)
        self.restart()

    def english(self):
        self.English.setChecked(True)
        self.Russian.setChecked(False)
        self.config['language'] = 'en'
        with open("data/numti.cfg", "w") as file:
            json.dump(self.config, file)
        self.restart()

    # Настройка изменения комбобокса (Configuring the combo box change)
    def change(self):
        if self.English.isChecked():
            if self.comboBox.currentIndex() == 0:
                self.pushButton.setText('Autosearch')
                self.pushButton.setEnabled(False)
                self.pushButton.hide()
                self.pushButton1.hide()
                self.pushButton2.hide()
                self.pushButton3.hide()
                self.plainTextEdit.setPlaceholderText('')
                self.lineEdit.setPlaceholderText('Enter the name/number')
                self.lineEdit.setText('')
                self.namedoc = ''
                self.label.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(False)
                self.plainTextEdit.setReadOnly(True)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.plainTextEdit.hide()
                self.tableWidget.show()
                self.setWindowTitle(self.comboBox.currentText())
                self.edit_text()
            elif self.comboBox.currentIndex() == 1:
                self.namedoc = ''
                self.pushButton.setText('Chose button')
                self.pushButton.setEnabled(False)
                self.pushButton.hide()
                self.pushButton1.show()
                self.pushButton2.show()
                self.pushButton3.show()
                self.plainTextEdit.setPlaceholderText('Enter additional information about the phone number.')
                self.lineEdit.setPlaceholderText('Enter the number')
                self.lineEdit.setText('')
                self.namedoc = ''
                self.label.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(True)
                self.plainTextEdit.setReadOnly(False)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.tableWidget.hide()
                self.plainTextEdit.show()
                self.setWindowTitle(self.comboBox.currentText())
            elif self.comboBox.currentIndex() == 2:
                self.pushButton.setText('Search')
                self.pushButton.setEnabled(True)
                self.pushButton.show()
                self.pushButton1.hide()
                self.pushButton2.hide()
                self.pushButton3.hide()
                self.plainTextEdit.setPlaceholderText('The information will be here')
                self.lineEdit.setPlaceholderText('Enter the number')
                self.lineEdit.setText('')
                self.namedoc = ''
                self.label.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(True)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.plainTextEdit.setReadOnly(True)
                self.tableWidget.hide()
                self.plainTextEdit.show()
                self.setWindowTitle(self.comboBox.currentText())
            elif self.comboBox.currentIndex() == 3:
                self.pushButton.setText('Search')
                self.pushButton.setEnabled(True)
                self.pushButton.show()
                self.pushButton1.hide()
                self.pushButton2.hide()
                self.pushButton3.hide()
                self.plainTextEdit.setPlaceholderText('')
                self.lineEdit.setPlaceholderText('Enter the name of the document to record')
                self.lineEdit.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(False)
                self.label.setEnabled(True)
                self.toolButton.setEnabled(True)
                self.plainTextEdit.setReadOnly(True)
                self.tableWidget.hide()
                self.plainTextEdit.hide()
                self.setWindowTitle(self.comboBox.currentText())
        elif self.Russian.isChecked():
            if self.comboBox.currentIndex() == 0:
                self.pushButton.setText('Автопоиск')
                self.pushButton.setEnabled(False)
                self.pushButton.hide()
                self.pushButton1.hide()
                self.pushButton2.hide()
                self.pushButton3.hide()
                self.plainTextEdit.setPlaceholderText('')
                self.lineEdit.setPlaceholderText('Введите имя/номер')
                self.lineEdit.setText('')
                self.namedoc = ''
                self.label.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(False)
                self.plainTextEdit.setReadOnly(True)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.plainTextEdit.hide()
                self.tableWidget.show()
                self.setWindowTitle(self.comboBox.currentText())
                self.edit_text()
            elif self.comboBox.currentIndex() == 1:
                self.pushButton.setText('Выбор кнопки')
                self.pushButton.setEnabled(False)
                self.pushButton.hide()
                self.pushButton1.show()
                self.pushButton2.show()
                self.pushButton3.show()
                self.plainTextEdit.setPlaceholderText('Введите информацию о номере')
                self.lineEdit.setPlaceholderText('Введите номер')
                self.lineEdit.setText('')
                self.namedoc = ''
                self.label.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(True)
                self.plainTextEdit.setReadOnly(False)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.tableWidget.hide()
                self.plainTextEdit.show()
                self.setWindowTitle(self.comboBox.currentText())
            elif self.comboBox.currentIndex() == 2:
                self.pushButton.setText('Поиск')
                self.pushButton.setEnabled(True)
                self.pushButton.show()
                self.pushButton1.hide()
                self.pushButton2.hide()
                self.pushButton3.hide()
                self.plainTextEdit.setPlaceholderText('Информация будет здесь')
                self.lineEdit.setPlaceholderText('Введите номер')
                self.lineEdit.setText('')
                self.namedoc = ''
                self.label.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(True)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.label.setEnabled(False)
                self.toolButton.setEnabled(False)
                self.plainTextEdit.setReadOnly(True)
                self.tableWidget.hide()
                self.plainTextEdit.show()
                self.setWindowTitle(self.comboBox.currentText())
            elif self.comboBox.currentIndex() == 3:
                self.pushButton.setText('Поиск')
                self.pushButton.setEnabled(True)
                self.pushButton.show()
                self.pushButton1.hide()
                self.pushButton2.hide()
                self.pushButton3.hide()
                self.plainTextEdit.setPlaceholderText('')
                self.lineEdit.setPlaceholderText('Введите имя документа для записи')
                self.lineEdit.setText('')
                self.plainTextEdit.setPlainText('')
                self.plainTextEdit.setEnabled(False)
                self.label.setEnabled(True)
                self.toolButton.setEnabled(True)
                self.plainTextEdit.setReadOnly(True)
                self.tableWidget.hide()
                self.plainTextEdit.hide()
                self.setWindowTitle(self.comboBox.currentText())

    # Настройка выбора файла (Configuring File Selection)
    def changedoc(self):
        if self.English.isChecked():
            self.namedoc = QFileDialog.getOpenFileName(self, 'Select a document', '/', 'Text document (*.txt)')[0]
            self.label.setText(self.namedoc)
        elif self.Russian.isChecked():
            self.namedoc = QFileDialog.getOpenFileName(self, 'Выберите документ', '/',
                                                       'Текстовый документ (*.txt)')[0]
            self.label.setText(self.namedoc)

    # Настройка вывода информации о программе (Setting up the output of information about the program)
    def aboutprogramm(self):
        if self.English.isChecked():
            QMessageBox.about(self, 'About program',
                              'The program uses a database with information that is freely available on the '
                              'Internet. \n \n The information is displayed either on the screen or in a text '
                              'document, depending on the selected mode. Information about the selected document '
                              'for processing is contained in the main window. We are not responsible for data '
                              'loss while using the text document mode. \n \n In case of an error when executing '
                              'the program, you will be notified.')
        elif self.Russian.isChecked():
            QMessageBox.about(self, 'О программе',
                              'Программа использует базу данных с информацией, '
                              'которая находится в свободном доступе в Интернете. \n \n'
                              'Информация отображается либо на экране, '
                              'либо в текстовом документе, в зависимости от выбранного режима. '
                              'Информация о выбранном документе для обработки '
                              'содержится в главном окне. Мы не несём ответственность за утерю данных во время '
                              'использования режима текстового документа. \n \n В случае ошибки при выполнении '
                              'приграммы вы будете оповещены.')

    # Настройка вывода помощи использования программы (Configuring the output by using the program)
    def howtousetheprogram(self):
        if self.English.isChecked():
            QMessageBox.about(self, 'How to use the program?',
                              '1. Select the operating mode. \n'
                              'There are several modes to choose from:\n'
                              'a) View known contacts.\n'
                              'b) Adding/Change/Deleting a contact.\n'
                              'c) Search by one number.\n'
                              'd) Text document search.\n \n'
                              '2 / a. Enter the name/number of the contact you want to find. \n'
                              '3 / a. All known contact information will be displayed in the table. \n \n'
                              '2 / b. Enter the name you want to write down to add or change the number, '
                              'or do not enter at all if you want to delete the number. \n'
                              '3 / b. Click on one of the buttons, depending on the required operation '
                              '(Add/Change/Delete).\n'
                              '4 / b. Done. The information is saved. \n \n'
                              '2 / c. Enter the phone number required for processing. \n'
                              '3 / c. Click on the "Search" button. \n'
                              '4 / c. Observe the reaction on the dashboard. \n'
                              '5 / c. If you need to find another phone number, repeat these steps.\n \n'
                              '2 / d. Select the file by clicking on the button with three dots. '
                              '(the name of the selected file will be shown next to the button) \n'
                              '3 / d. Enter the name of the document to be recorded. \n'
                              '4 / d. Click on the "Search" button. \n'
                              '5 / d. In case of problems with the processing of the number, '
                              'an informational notification will appear. \n'
                              '6 / d. You will be notified of the completion of the operation. \n'
                              '7 / d. All information is stored in the text document that you entered. \n \n')
        elif self.Russian.isChecked():
            QMessageBox.about(self, 'Как использовать программу?',
                              '1. Выберите режим работы. \n'
                              'Есть несколько режимов на выбор:\n'
                              'а) Просмотр известных контактов.\n'
                              'б) Добавление/Изменение/Удаление контакта.\n'
                              'в) Поиск по одному номеру.\n'
                              'г) Поиск по текстовому документу.\n \n'
                              '2 / а. Введите имя/номер контакта, который хотите найти. \n'
                              '3 / а. Вся известная информация о контактах будет отображена в таблице. \n \n'
                              '2 / б. Введите имя, которое вы хотите записать для добавления или изменения номера, '
                              'или не вводите вовсе, если хотите удалить номер. \n'
                              '3 / б. Нажмите на одну из кнопок, в зависимости от необходимой операции '
                              '(Добавить/Изменить/Удалить). \n'
                              '4 / б. Готово. Информация сохранена. \n \n'
                              '2 / в. Введите номер телефона, необходимый для обработки. \n'
                              '3 / в. Нажмите на кнопку "Поиск". \n'
                              '4 / в. Наблюдайте за реакцией на приборной панели. \n'
                              '5 / в. Если вам нужно найти другой номер телефона, повторите эти действия.\n \n'
                              '2 / г. Выберите файл, нажав на кнопку с тремя точками. '
                              '(имя выбранного файла будет показано рядом с кнопкой) \n'
                              '3 / г. Введите имя документа, который будет записан. \n'
                              '4 / г. Нажмите на кнопку "Поиск". \n'
                              '5 / г. В случае возникновения проблем с обработкой номера, '
                              'появится информационное уведомление. \n'
                              '6 / г. Вы будете уведомлены о завершении операции. \n'
                              '7 / г. Вся информация хранится в текстовом документе,  который вы ввели. \n \n')

    # Главное действие, поиск или запись доп. информации (Main action, search or recording of additional information)
    def run(self):
        # Настройка поиска по одному номеру (Setting up a search by one number)
        if self.comboBox.currentIndex() == 2:
            check = checknum.search_by_one_number(self.lineEdit.text(), self.config['language'],
                                                  self.config['translating'])
            if check == 404:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", f"{self.lineEdit.text()}: Unknown number.",
                                         QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", f"{self.lineEdit.text()}: Неизвестный номер.",
                                         QMessageBox.Ok)
            elif check == 400:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", f"{self.lineEdit.text()}: Wrong number dialed.",
                                         QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", f"{self.lineEdit.text()}: Неправильно набран номер.",
                                         QMessageBox.Ok)
            elif check == 406:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "No number entered.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Номер не введён.", QMessageBox.Ok)
            elif check == 499:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "No connection.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Нет соединения.", QMessageBox.Ok)
            elif check == 522:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "Critical error.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Критическая ошибка.", QMessageBox.Ok)
            else:
                self.plainTextEdit.setPlainText(check)
        elif self.comboBox.currentIndex() == 3:
            check = checknum.search_from_a_text_document(self.namedoc, self.lineEdit.text(),
                                                         self.config['language'], self.config['translating'])
            if not check:
                # Информация о законченной операции (Information about the completed operation)
                if self.English.isChecked():
                    QMessageBox.information(self, "Done!", "The information is saved.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.information(self, "Готово!", "Информация сохранена.", QMessageBox.Ok)
            elif check == 206:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Attention!", "One of the entered numbers "
                                                             "is entered incorrectly. "
                                                             "The known information is "
                                                             "indicated in the document.",
                                         QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Внимание!", "Один из введенных номеров"
                                                            "введен неправильно."
                                                            "Известная информация"
                                                            "указана в документе.",
                                         QMessageBox.Ok)
                # Действия исключений (Exception Actions)
            elif check == 406:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "There is no document for reading/writing.",
                                         QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Не найден документ для чтения/записи.",
                                         QMessageBox.Ok)
            elif check == 499:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "No connection.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Нет соединения.", QMessageBox.Ok)
            elif check == 522:
                if self.English.isChecked():
                    QMessageBox.critical(self, "Warning!", "Critical error.", QMessageBox.Ok)
                elif self.Russian.isChecked():
                    QMessageBox.critical(self, "Предупреждение!", "Критическая ошибка.", QMessageBox.Ok)

    def addcontact(self):
        check = checknum.add_contact(self.lineEdit.text(), self.plainTextEdit.toPlainText())
        if not check:
            if self.English.isChecked():
                QMessageBox.information(self, "Done!", "The information is saved.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.information(self, "Готово!", "Информация сохранена.", QMessageBox.Ok)
        # Действия исключений (Exception Actions)
        elif check == 4001:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Invalid number entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Введен неверный номер.", QMessageBox.Ok)
        elif check == 4002:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "No number entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Номер не введён.", QMessageBox.Ok)
        elif check == 4003:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Information not entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Информация не введена.", QMessageBox.Ok)
        elif check == 4004:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "This number is already in the contacts.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Этот номер уже есть в контактах.", QMessageBox.Ok)
        elif check == 522:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Critical error.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Критическая ошибка.", QMessageBox.Ok)

    def editcontact(self):
        check = checknum.edit_contact(self.lineEdit.text(), self.plainTextEdit.toPlainText())
        if not check:
            if self.English.isChecked():
                QMessageBox.information(self, "Done!", "The information is saved.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.information(self, "Готово!", "Информация сохранена.", QMessageBox.Ok)
        # Действия исключений (Exception Actions)
        elif check == 4001:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Invalid number entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Введен неверный номер.", QMessageBox.Ok)
        elif check == 4002:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "No number entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Номер не введён.", QMessageBox.Ok)
        elif check == 4003:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Information not entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Информация не введена.", QMessageBox.Ok)
        elif check == 4004:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "There is no such number in contacts.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Такого номера нет в контактах.", QMessageBox.Ok)
        elif check == 522:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Critical error.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Критическая ошибка.", QMessageBox.Ok)

    def deletecontact(self):
        check = checknum.delete_contact(self.lineEdit.text())
        if not check:
            if self.English.isChecked():
                QMessageBox.information(self, "Done!", "The information is saved.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.information(self, "Готово!", "Информация сохранена.", QMessageBox.Ok)
        # Действия исключений (Exception Actions)
        elif check == 4001:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Invalid number entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Введен неверный номер.", QMessageBox.Ok)
        elif check == 4002:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "No number entered.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Номер не введён.", QMessageBox.Ok)
        elif check == 4004:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "There is no such number in contacts.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Такого номера нет в контактах.", QMessageBox.Ok)
        elif check == 522:
            if self.English.isChecked():
                QMessageBox.critical(self, "Warning!", "Critical error.", QMessageBox.Ok)
            elif self.Russian.isChecked():
                QMessageBox.critical(self, "Предупреждение!", "Критическая ошибка.", QMessageBox.Ok)

# Инициализация ошибок (Error Initialization)
class NumError(Exception):
    pass


class InfoError(Exception):
    pass


class FullError(Exception):
    pass


class NoNumError(Exception):
    pass


# Перевод C'шных ошибов в Python'овские (Translating C errors to Python)
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# Точка входа (Entry point)
if __name__ == '__main__':
    sys.argv[0] = 'Numti'
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    win = Window()
    win.show()
    sys.exit(app.exec())
