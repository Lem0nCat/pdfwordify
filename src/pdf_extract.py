import fitz  # PyMuPDF для извлечения изображений

# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure

import pdfplumber   # Для извлечения текста из таблиц в PDF

import os   # Для удаления дополнительно созданных файлов

from Classes.Elements import * # Собственные классы с элементами
from Classes.Font import Font

from Tools.config import TABLE_SETTINGS, IMAGES_PATH

from Tools.table_extract import *
from Tools.text_extract import *
from Tools.image_extract import *


def is_landscape_orientation(page_object):
    # Получаем размеры страницы
    width, height = page_object.rect.width, page_object.rect.height
    
    if width > height:
        return True
    return False

def delete_png_files(directory):
    # Перебор всех файлов в директории
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            file_path = os.path.join(directory, filename)
            # Удаление файла
            os.remove(file_path)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #   Извлечение информации после разбиения файла на объекты классов    # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
def extract_all(path_to_pdf):
    # Используем fitz для извлечения изображений
    pdf_fitz = fitz.open(path_to_pdf)  
    # Используем pdfplumber для извлечения таблиц
    pdf_plmb = pdfplumber.open(path_to_pdf)

    # Создаём словарь для извлечения текста из каждого изображения
    content_per_page = []
    
    # Создаем переменную, которая будет хранить часто используемый шрифт в документе
    default_font = Font()
    fonts = []

    # Цикл по страницам
    for pagenum, page in enumerate(extract_pages(path_to_pdf)):
        page_content = []
        extracted_tables = []
        
        image_index = 0 # Задаем индекс для прохожения по изображениям
        images_paths = extract_images(pdf_fitz, pagenum)
        
        # Текущая страница
        page_tables = pdf_plmb.pages[pagenum]
        # Нахождение таблиц на странице
        tables = page_tables.find_tables(table_settings=TABLE_SETTINGS)
        
        # Индекс таблицы на странице (если -1, то таблиц нет)
        table_index = 0 if tables else -1

        # Извлечение таблиц из страницы
        for table_num in range(len(tables)):
            # Извлеките информацию из таблицы
            table = extract_table(path_to_pdf, pagenum, table_num)
            # Добавление преобразованной таблицы в список
            extracted_tables.append(table)

        # Получение всех элементов на странице
        page_elements = [(element.y1, element) for element in page._objs]
        # Сортировка всех элементов по мере их расположения на странице
        page_elements.sort(key=lambda a: a[0], reverse=True)


        # Цикл по компонентам на странице
        for i, component in enumerate(page_elements):
            # Извлечение элемента макета страницы
            element = component[1]

            # Проверка элемента на наличие таблиц
            if table_index != -1 and is_element_inside_any_table(element, page, tables):
                table_found = find_table_for_element(element,page ,tables)
                if table_found == table_index:   
                    table = TableElement(extracted_tables[table_index])
                        
                    page_content.append(table)
                    table_index += 1
                # Пропустить эту итерацию, потому что содержимое этого элемента было извлечено из таблиц
                continue

            # if not is_element_inside_any_table(element, page, tables):
            # Check if the element is text element
            if isinstance(element, LTTextContainer):
                # Use the function to extract the text and format for each text element
                line_text, font = text_extraction(element)
                fonts.append(font)
                
                text_element = TextElement(line_text, font)

                # Добавляем в содержание страницы текстовый объект
                page_content.append(text_element)


            # Проверка элемента на изображение
            if isinstance(element, LTFigure):                  
                # Извлечение текста из изображения
                image_text = image_to_text(images_paths[image_index])
                image_index += 1

                if (len(fonts) > 2):
                    default_font = Font.get_default_font(fonts)
                    font = default_font
                elif fonts:
                    font = fonts[-1]
                else:
                    font = Font()
            
                image_element = ImageElement(image_text, font)
                page_content.append(image_element)

        # Добавляем элементы страницы в общий список
        content_per_page.append({
            "page_content": page_content,
            "landscape_orientation": is_landscape_orientation(pdf_fitz[pagenum])
        })


    # Закрываем объект файла pdf
    pdf_fitz.close()
    pdf_plmb.close()

    # Удаляем созданные дополнительные файлы
    delete_png_files(IMAGES_PATH)

    return content_per_page