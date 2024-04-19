import camelot  # Для извлечения текста из таблиц в PDF
from collections import defaultdict

import math

from Tools.config import TABLE_SETTINGS

from Tools.image_extract import ConversionBackend



# # # # # # # # # # # # # # # # # # # # #
# #   Извлечение текста из таблиц   # # #
# # # # # # # # # # # # # # # # # # # # #

def extract_table_camelot(pdf_path, flavor='lattice'):  
    # Создаем словарь с аргументами по умолчанию
    args = {
        'backend': ConversionBackend(),
        'strip_text': '\n',
        'pages': 'all',
        'flavor': flavor
    }
    
    # Добавляем аргументы, которые зависят от значения flavor
    if flavor != 'stream':
        args['line_scale'] = 40
        args['copy_text'] = ['h']

    # Вызываем функцию с динамически сформированными аргументами
    tables = camelot.read_pdf(pdf_path, **args)
    

    # Сгруппировать таблицы по страницам
    page_tables = defaultdict(list)
    for table in tables:
        page_tables[table.page].append(table)
    return page_tables


def normalize_table_coordinates(table):
    x0, y0, x1, y1 = table._bbox
    x0, y0 = math.floor(x0), math.floor(y0)
    x1, y1 = math.ceil(x1), math.ceil(y1)
    return x0, y0, x1, y1


# Function to find the table for a given element
def find_table_for_element(element, tables):
    x0, y0, x1, y1 = element.bbox

    for i, table in enumerate(tables):
        table_x0, table_y0, table_x1, table_y1 = table._bbox
        if (x0 >= table_x0 and x1 <= table_x1) and (y0 >= table_y0 and y1 <= table_y1):
            return i  # Return the index of the table
    return None

# Create a function to check if the element is in any tables present in the page
def is_element_inside_any_table(element, tables):
    x0, y0, x1, y1 = element.bbox

    for table in tables:
        table_x0, table_y0, table_x1, table_y1 = normalize_table_coordinates(table)
        if (x0 >= table_x0 and x1 <= table_x1) and (y0 >= table_y0 and y1 <= table_y1):
            return True  # Return the index of the table
    return False

