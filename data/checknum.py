"""Импортирование библиотек (Importing libraries)"""
import sqlite3
import time

from googletrans import Translator
from httpcore._exceptions import ConnectTimeout, CloseError, ConnectError


def only_num(s: str) -> str:
    return ''.join([i for i in s if i.isdigit()])


def search_by_one_number(text: str, locale: str, translate: bool) -> (int, str):
    """Выполнение поиска по одному номеру (Performing a search by one number)"""
    try:
        # Считывание с главной строки (Reading from the main line)
        # Проверка на правильность номера (Checking for the correctness of the number)
        num = only_num(text)
        if not num:
            raise NoNumError
        if num[0] == '8' and len(num) == 11 and text.strip()[0] != '+':
            num = f"7{num[1:]}"
        # Работа с базами данных, считывание нужных параметров и запись их в переменную
        # (Working with databases, reading the necessary parameters and writing them to a variable)
        con = sqlite3.connect('data/checkbd.db')
        cur = con.cursor()
        cur.execute(f"""SELECT code, country_{locale}, timezone FROM countries""")
        bdcountry = cur.fetchall()
        cur.execute(f"""SELECT code, operator_{locale}, region_{locale} FROM rusnummob 
                        JOIN operators ON operators.id = rusnummob.operator
                        JOIN regions ON regions.id = rusnummob.region""")
        rusmob = cur.fetchall()
        cur.execute(f"""SELECT code, region_{locale} FROM rusnumgor 
                        JOIN regions ON regions.id = rusnumgor.region""")
        rusgor = cur.fetchall()
        cur.execute(f"""SELECT nmb, info FROM postscriptum""")
        pstscrptm = cur.fetchall()
        # Проверка на неизвестность номера (Checking for unknown numbers)
        flag = True
        # Нахождение информации о номере (Finding information about the number)
        # Проверка на правильность набранного номера (Checking for the correctness of the dialed number)
        if num.isdigit():
            info = []
            if 15 > len(num) > 8:
                # Поиск по стране (Search by country)
                for cdc in bdcountry:
                    if num.startswith(cdc[0]):
                        info.append([cdc[1], cdc[2]])
                        # Проверка на принадлежность к России (Verification of belonging to Russia)
                        if num.startswith('79'):
                            # Поиск на правильность Российского номера
                            # (Search for the correctness of the Russian number)
                            if len(num) == 11:
                                # Нахождение оператора и региона сотового номера
                                # (Finding the operator and the region of the cell number)
                                for cdm in rusmob:
                                    if num[1:].startswith(cdm[0]):
                                        if locale == 'en':
                                            info.append([f'Operator: {cdm[1]}',
                                                         f'Region: {cdm[2]}'])
                                        elif locale == 'ru':
                                            info.append([f'Оператор: {cdm[1]}',
                                                         f'Регион: {cdm[2]}'])
                                        flag = False
                                        break
                                if flag:
                                    if locale == 'en':
                                        info.append(['Operator: Unknown', 'Region: Unknown'])
                                    elif locale == 'ru':
                                        info.append(['Оператор: Неизвестно', 'Регион: Неизвестно'])
                            else:
                                info = []
                        elif num.startswith('7'):
                            if len(num) == 11:
                                # Нахождение региона городского номера
                                # (Finding the region of the city number)
                                for cdg in rusgor:
                                    if num[1:].startswith(cdg[0]):
                                        if locale == 'en':
                                            info.append([f'Region: {cdg[1]}'])
                                        elif locale == 'ru':
                                            info.append([f'Регион: {cdg[1]}'])
                                        flag = False
                                        break
                                if flag:
                                    if locale == 'en':
                                        info.append(['Region: Unknown'])
                                    elif locale == 'ru':
                                        info.append(['Регион: Неизвестно'])
                            else:
                                info = []
            # Поиск доп. информации о номере (Search for additional information about the room)
            for i in pstscrptm:
                if i[0] == num:
                    if translate:
                        translation = Translator().translate(f'{i[1]}', dest=locale)
                        info.append([f'P.s. {translation.text}'])
                    else:
                        info.append([f'P.s. {i[1]}'])
            # Проверка на нахождение информации (Checking for finding information)
            if not info:
                con.close()
                return 404
            else:
                # Запись найденной информации (Recording the information found)
                res = []
                for i in info:
                    if i.count('') > 0:
                        i.remove('')
                    res.append('\n'.join(i))
                result = '\n'.join(res)
                con.close()
                return f'+{num}: {result}\n'
        else:
            con.close()
            return 400
    # Действия исключений (Exception Actions)
    except NoNumError:
        return 406
    except ConnectError or ConnectTimeout or CloseError:
        return 499
    except Exception as e:
        print(f'{e} | {type(e)}')
        return 522


def search_from_a_text_document(readdoc: str, writedoc: str, locale: str, translate: bool) -> int:
    """Настройка поиска из текстового документа (Setting up a search from a text document)"""
    try:
        # Считывание из документа и преобразование в корректный номер
        # (Reading from the document and converting to the correct number)
        with open(f'{readdoc}', encoding='utf-8') as f:
            text = []
            for i in f.readlines():
                num = only_num(i)
                if not num:
                    continue
                if num[0] == '8' and len(num) == 11 and i.strip()[0] == '+':
                    text.append(f"7{num[1:]}")
                else:
                    text.append(num.lstrip('+'))
        # Работа с базами данных, считывание нужных параметров и запись их в переменную
        # (Reading from the document and converting to the correct number)
        con = sqlite3.connect('data/checkbd.db')
        cur = con.cursor()
        cur.execute(f"""SELECT code, country_{locale}, timezone FROM countries""")
        bdcountry = cur.fetchall()
        cur.execute(f"""SELECT code, operator_{locale}, region_{locale} FROM rusnummob 
                        JOIN operators ON operators.id = rusnummob.operator
                        JOIN regions ON regions.id = rusnummob.region""")
        rusmob = cur.fetchall()
        cur.execute(f"""SELECT code, region_{locale} FROM rusnumgor 
                        JOIN regions ON regions.id = rusnumgor.region""")
        rusgor = cur.fetchall()
        cur.execute(f"""SELECT nmb, info FROM postscriptum""")
        pstscrptm = cur.fetchall()
        # Информирование: был ли варнинг (Informing: was there a warning)
        wrng = False
        # Запись в исходный файл (Writing to the source file)
        if writedoc[-4::] == '.txt':
            sdoc = writedoc
        elif writedoc.strip():
            sdoc = f'{writedoc}.txt'
        else:
            sdoc = f'{readdoc[readdoc.rfind("/"):readdoc.rfind(".")]}-parsed.txt'
        with open(f'{readdoc[:readdoc.rfind("/") + 1]}{sdoc}', 'w',
                  encoding='utf-8') as f:
            # Обработка всех значений (Processing all values)
            for num in text:
                flag = True
                # Проверка на правильность номера (Checking for the correctness of the number)
                if num.isdigit():
                    info = []
                    if 15 > len(num) > 8:
                        # Поиск по стране (Search by country)
                        for cdc in bdcountry:
                            if num.startswith(cdc[0]):
                                info.append([cdc[1], cdc[2]])
                                # Проверка на принадлежность к России
                                # (Verification of belonging to Russia)
                                if num.startswith('79'):
                                    # Проверка на правильность Российского номера
                                    # (Checking for the correctness of the Russian number)
                                    if len(num) == 11:
                                        for cdm in rusmob:
                                            if num[1:].startswith(cdm[0]):
                                                if locale == 'en':
                                                    info.append([f'Operator: {cdm[1]}',
                                                                 f'Region: {cdm[2]}'])
                                                elif locale == 'ru':
                                                    info.append([f'Оператор: {cdm[1]}',
                                                                 f'Регион: {cdm[2]}'])
                                                flag = False
                                                break
                                        if flag:
                                            if locale == 'en':
                                                info.append(['Operator: Unknown', 'Region: Unknown'])
                                            elif locale == 'ru':
                                                info.append(
                                                    ['Оператор: Неизвестно', 'Регион: Неизвестно'])
                                    else:
                                        info = []
                                elif num.startswith('7'):
                                    if len(num) == 11:
                                        for cdg in rusgor:
                                            if num[1:].startswith(cdg[0]):
                                                if locale == 'en':
                                                    info.append([f'Region: {cdg[1]}'])
                                                elif locale == 'ru':
                                                    info.append([f'Регион: {cdg[1]}'])
                                                flag = False
                                                break
                                        if flag:
                                            if locale == 'en':
                                                info.append(['Region: Unknown'])
                                            elif locale == 'ru':
                                                info.append(['Регион: Неизвестно'])
                                    else:
                                        info = []
                    # Поиск доп. информации (Search for additional information)
                    for i in pstscrptm:
                        if i[0] == num:
                            if translate:
                                translation = Translator().translate(f'{i[1]}', dest=locale)
                                info.append([f'P.s. {translation.text}'])
                            else:
                                info.append([f'P.s. {i[1]}'])
                    # Проверка на наличие информации (Checking for information)
                    if not info:
                        if locale == 'en':
                            f.write(f'+{num}: Unknown number \n')
                        elif locale == 'ru':
                            f.write(f'+{num}: Неизвестный номер \n')
                    else:
                        # Запись найденной информации в документ
                        # (Recording the information found in the document)
                        res = []
                        for i in info:
                            if i.count('') > 0:
                                i.remove('')
                            res.append('\n'.join(i))
                        result = '\n'.join(res)
                        f.write(f'+{num}: {result}\n')
                else:
                    wrng = True
                    if locale == 'en':
                        f.write(f'+{num}: Wrong number dialed \n')
                    elif locale == 'ru':
                        f.write(f'+{num}: Неправильно введен номер \n')
                f.write('\n')
        con.close()
        # Информация о законченной операции (Information about the completed operation)
        if wrng:
            return 206
        return 0
    # Действия исключений (Exception Actions)
    except AttributeError:
        return 406
    except ConnectError or ConnectTimeout or CloseError:
        return 499
    except Exception as e:
        print(f'{e} | {type(e)}')
        return 522


def add_contact(text: str, information: str) -> int:
    """Выполнение записи в контактную книгу (Making an entry in the contact book)"""
    try:
        # Считывание и обработка данных (Data reading and processing)
        # Проверка на правильность номера (Checking for the correctness of the number)
        num = only_num(text)
        if not num:
            raise NoNumError
        if num[0] == '8' and len(num) == 11 and text.strip()[0] != '+':
            num = f"7{num[1:]}"
        # Работа с базами данных, считывание нужных параметров и запись их в переменную
        # (Working with databases, reading the necessary parameters and writing them to a variable)
        con = sqlite3.connect('data/checkbd.db')
        cur = con.cursor()
        know = cur.execute(f"""SELECT nmb FROM postscriptum""").fetchall()
        # Проверка на нахождение номера уже в базе данных
        # (Checking if the number is already in the database)
        hv = False
        for i in know:
            if num == i[0]:
                hv = True
        if hv:
            raise ContactError
        else:
            # Запись информации если номера нет в базе данных
            # (Recording information if the number is not in the database)
            if information:
                cur.execute('INSERT INTO postscriptum(nmb, info) VALUES (?,?)', [num, information])
                con.commit()
            else:
                raise InfoError
        con.close()
        return 0
    # Действия исключений (Exception Actions)
    except NoNumError:
        return 4001
    except InfoError:
        return 4002
    except ContactError:
        return 4003
    except Exception as e:
        print(f'{e} | {type(e)}')
        return 522


def edit_contact(text: str, information: str) -> int:
    """Выполнение редактирования контактной книги (Performing Contact Book editing)"""
    try:
        # Считывание и обработка данных (Data reading and processing)
        # Проверка на правильность номера (Checking for the correctness of the number)
        num = only_num(text)
        if not num:
            raise NoNumError
        if num[0] == '8' and len(num) == 11 and text.strip()[0] != '+':
            num = f"7{num[1:]}"
        # Работа с базами данных, считывание нужных параметров и запись их в переменную
        # (Working with databases, reading the necessary parameters and writing them to a variable)
        con = sqlite3.connect('data/checkbd.db')
        cur = con.cursor()
        know = cur.execute(f"""SELECT nmb FROM postscriptum""").fetchall()
        # Проверка на нахождение номера уже в базе данных
        # (Checking if the number is already in the database)
        hv = False
        for i in know:
            if num == i[0]:
                hv = True
        if hv:
            if information:
                # Обновление информации если номер уже есть в базе данных
                # (Updating information if the number is already in the database)
                cur.execute("""UPDATE postscriptum
                                    SET info = (?) 
                                        WHERE nmb = (?)""", [information, num])
                con.commit()
            else:
                raise InfoError
        else:
            raise ContactError
        con.close()
        return 0
    # Действия исключений (Exception Actions)
    except NoNumError:
        return 4001
    except InfoError:
        return 4002
    except ContactError:
        return 4003
    except Exception as e:
        print(f'{e} | {type(e)}')
        return 522


def delete_contact(text: str) -> int:
    """Выполнение удаления из книги контактов (Performing deletion from the contact book)"""
    try:
        # Считывание и обработка данных (Data reading and processing)
        # Проверка на правильность номера (Checking for the correctness of the number)
        num = only_num(text)
        if not num:
            raise NoNumError
        if num[0] == '8' and len(num) == 11 and text.strip()[0] != '+':
            num = f"7{num[1:]}"
        # Работа с базами данных, считывание нужных параметров и запись их в переменную
        # (Working with databases, reading the necessary parameters and writing them to a variable)
        con = sqlite3.connect('data/checkbd.db')
        cur = con.cursor()
        know = cur.execute(f"""SELECT nmb FROM postscriptum""").fetchall()
        # Проверка на нахождение номера уже в базе данных
        # (Checking if the number is already in the database)
        hv = False
        for i in know:
            if num == i[0]:
                hv = True
        if hv:
            # Удаление информации если номер есть в базе данных
            # (Deleting information if the number is in the database)
            cur.execute("""DELETE FROM postscriptum
                                    WHERE nmb = (?)""", [num])
            con.commit()
        else:
            raise ContactError
        con.close()
        return 0
    # Действия исключений (Exception Actions)
    except NoNumError:
        return 4001
    except ContactError:
        return 4003
    except Exception as e:
        print(f'{e} | {type(e)}')
        return 522


def my_contact(text: str, locale: str, translate: bool) -> (int, list):
    """Выполнение поиска внутри книги контактов (Performing a search inside the contact book)"""
    try:
        # Считывание с главной строки (Reading from the main line)
        # Удаление лишних символов и проверка на корректность
        # (Removing extra characters and checking for correctness)
        text = text.strip()
        num = only_num(text)
        if text and text[0] != '+' and num and num[0] == '8' and len(num) == 11:
            num = f"7{num[1:]}"
        # Работа с базами данных, считывание нужных параметров и запись их в переменную
        # (Working with databases, reading the necessary parameters and writing them to a variable)
        con = sqlite3.connect('data/checkbd.db')
        cur = con.cursor()
        cur.execute(f"""SELECT code, country_{locale}, timezone FROM countries""")
        bdcountry = cur.fetchall()
        cur.execute(f"""SELECT code, operator_{locale}, region_{locale} FROM rusnummob 
                        JOIN operators ON operators.id = rusnummob.operator
                        JOIN regions ON regions.id = rusnummob.region""")
        rusmob = cur.fetchall()
        cur.execute(f"""SELECT code, region_{locale} FROM rusnumgor 
                        JOIN regions ON regions.id = rusnumgor.region""")
        rusgor = cur.fetchall()
        cur.execute(f"""SELECT * FROM postscriptum""")
        pstscrptm = cur.fetchall()
        rows = []
        for row in pstscrptm:
            if num in row[1] or text.lower() in row[2].lower():
                if translate:
                    translated = Translator().translate(f'{row[2]}', dest=locale)
                    rows.append([row[0], f'+{row[1]}', translated.text, ''])
                else:
                    rows.append([row[0], f'+{row[1]}', row[2], ''])
        # Проверка на неизвестность номера (Checking for unknown numbers)
        flag = True
        # Нахождение информации о номере (Finding information about the number)
        # Проверка на правильность набранного номера (Checking for the correctness of the dialed number)
        res_search = rows
        for n, row in enumerate(rows):
            num = row[1].lstrip('+')
            info = []
            if 15 > len(num) > 8:
                # Поиск по стране (Search by country)
                for cdc in bdcountry:
                    if ',' in cdc[0]:
                        for i in cdc[0].split(', '):
                            if num.startswith(i):
                                info.append([cdc[1], cdc[2]])
                                break
                    else:
                        if num.startswith(cdc[0]):
                            info.append([cdc[1], cdc[2]])
                            # Проверка на принадлежность к России (Verification of belonging to Russia)
                            if num.startswith('79'):
                                # Поиск на правильность Российского номера
                                # (Search for the correctness of the Russian number)
                                if len(num) == 11:
                                    # Нахождение оператора и региона сотового номера
                                    # (Finding the operator and the region of the cell number)
                                    for cdm in rusmob:
                                        if num[1:].startswith(cdm[0]):
                                            if locale == 'en':
                                                info.append([f'Operator: {cdm[1]}',
                                                             f'Region: {cdm[2]}'])
                                            elif locale == 'ru':
                                                info.append([f'Оператор: {cdm[1]}',
                                                             f'Регион: {cdm[2]}'])
                                            flag = False
                                            break
                                    if flag:
                                        if locale == 'en':
                                            info.append(['Operator: Unknown', 'Region: Unknown'])
                                        elif locale == 'ru':
                                            info.append(['Оператор: Неизвестно', 'Регион: Неизвестно'])
                                else:
                                    info = []
                            elif num.startswith('7'):
                                if len(num) == 11:
                                    # Нахождение региона городского номера
                                    # (Finding the region of the city number)
                                    for cdg in rusgor:
                                        if num[1:].startswith(cdg[0]):
                                            if locale == 'en':
                                                info.append([f'Region: {cdg[1]}'])
                                            elif locale == 'ru':
                                                info.append([f'Регион: {cdg[1]}'])
                                            flag = False
                                            break
                                    if flag:
                                        if locale == 'en':
                                            info.append(['Region: Unknown'])
                                        elif locale == 'ru':
                                            info.append(['Регион: Неизвестно'])
                                else:
                                    info = []
            # Проверка на нахождение информации (Checking for finding information)
            if not info:
                if locale == 'en':
                    res_search[n][3] = 'Not info'
                elif locale == 'ru':
                    res_search[n][3] = 'Нет информации'
            else:
                # Запись найденной информации (Recording the information found)
                res = []
                for i in info:
                    if i.count('') > 0:
                        i.remove('')
                    res.append('; '.join(i))
                result = '; '.join(res)
                res_search[n][3] = result
            flag = True
        con.close()
        return res_search
    # Действия исключений (Exception Actions)
    except ConnectError or ConnectTimeout or CloseError:
        return 499
    # except Exception as e:
    #     print(f'{e} | {type(e)}')
    #     return 522


"""Инициализация ошибок (Error Initialization)"""


class InfoError(Exception):
    pass


class ContactError(Exception):
    pass


class NoNumError(Exception):
    pass


"""Точка входа теста (Test entry point)"""
if __name__ == '__main__':
    st = time.time()
    # test code
    print(time.time() - st)
