import camelot  # Для извлечения текста из таблиц в PDF
from collections import defaultdict

import math

from Tools.image_extract import ConversionBackend


# # # # # # # # # # # # # # # # # # # # #
# #   Извлечение текста из таблиц   # # #
# # # # # # # # # # # # # # # # # # # # #

def extract_table_camelot(pdf_path, flavor='lattice'):  
    """
    Извлекает все таблицы из PDF документа.
    
    Args:
        pdf_path: Путь до PDF документа.
        flavor (str, optional): Режим извлечения таблиц (lattice, stream, None). По умолчанию 'lattice'.
        
    Returns:
        defaultdict of camelot.core.Table: Список всех извлеченных таблиц из документа, которые сгруппированы по страницам.
    """
    args = {
        'backend': ConversionBackend(),
        'pages': 'all',
        'flavor': flavor
    }
    
    # Добавляем аргументы, которые зависят от значения lattice
    if flavor == 'lattice':
        args['line_scale'] = 30

    # Вызываем функцию с динамически сформированными аргументами
    tables = camelot.read_pdf(pdf_path, **args)
    
    # Сгруппировать таблицы по страницам
    page_tables = defaultdict(list)
    for table in tables:
        page_tables[table.page].append(table)
    return page_tables


def normalize_table_coordinates(table):
    """
    Округляет координаты таблицы.
    
    Args: 
        table (camelot.core.Table): Таблица camelot.
    
    Returns:
        (int, int, int, int): Координаты таблицы.
    """
    x0, y0, x1, y1 = table._bbox
    x0, y0 = math.floor(x0), math.floor(y0)
    x1, y1 = math.ceil(x1), math.ceil(y1)
    return x0, y0, x1, y1

def get_table_index(element, tables):
    """
    Функция для нахождения таблицы для заданного элемента.
    
    Args:
        element (pdfminer.layout): Элемент внутри страницы PDF документа.
        tables (list of camelot.core.TableList): Список объектов класса таблицы camelot.
    
    Returns:
        int or None: Индекс таблицы, содержащей элемент, если таковой имеется. Возвращает None, если элемент не содержится ни в одной таблице.
    """
    x0, y0, x1, y1 = element.bbox

    for i, table in enumerate(tables):
        table_x0, table_y0, table_x1, table_y1 = table._bbox
        if (x0 >= table_x0 and x1 <= table_x1) and (y0 >= table_y0 and y1 <= table_y1):
            return i  # Возвращаем индекс таблицы
    return None

def is_element_inside_any_table(element, tables):
    """
    Проверка на наличие элемента в какой-либо таблицу
    
    Args:
        element (pdfminer.layout): Элемент внутри страницы PDF документа.
        tables (list of camelot.core.TableList): Список объектов класса таблицы camelot.
    
    Returns:
        bool: Возвращает True, если элемент содержится в одной из таблиц.
    """
    x0, y0, x1, y1 = element.bbox

    for table in tables:
        table_x0, table_y0, table_x1, table_y1 = normalize_table_coordinates(table)
        if (x0 >= table_x0 and x1 <= table_x1) and (y0 >= table_y0 and y1 <= table_y1):
            return True  # Возвращаем индекс таблицы
    return False
