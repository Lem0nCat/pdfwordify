import PyPDF2   # Для считывания PDF

# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure

import pdfplumber   # Для извлечения текста из таблиц в PDF

import os   # Для удаления дополнительно созданных файлов

from Classes.Elements import * # Собственные классы с элементами
from Classes.Font import Font

from Tools.config import TABLE_SETTINGS

from Tools.table_extract import *
from Tools.text_extract import *
from Tools.image_extract import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #   Извлечение информации после разбиения файла на объекты классов    # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
def extract_all(path_to_pdf):
    # создаём объект файла PDF
    pdfFileObj = open(path_to_pdf, 'rb')
    # создаём объект считывателя PDF
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)

    # Создаём словарь для извлечения текста из каждого изображения
    content_per_page = []
    
    # Создаем переменную, которая будет хранить часто используемый шрифт в документе
    default_font = Font()
    fonts = []

    # Цикл по страницам
    for pagenum, page in enumerate(extract_pages(path_to_pdf)):
        # Объект страницы
        pageObj = pdfReaded.pages[pagenum]

        page_content = []
        extracted_tables = []
        
        # Индекс таблицы на странице (если -1, то таблиц нет)
        table_index = -1
        # Открытие pdf файла
        pdf = pdfplumber.open(path_to_pdf)
        # Текущая страница
        page_tables = pdf.pages[pagenum]
        # Нахождение таблиц на странице
        tables = page_tables.find_tables(table_settings=TABLE_SETTINGS)
        
        if len(tables) != 0:
            table_index = 0

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
            if table_index == -1:
                pass
            else:
                if is_element_inside_any_table(element, page, tables):
                    table_found = find_table_for_element(element,page ,tables)
                    if table_found == table_index and table_found != None:   
                        table = TableElement(extracted_tables[table_index])
                         
                        page_content.append(table)
                        table_index += 1
                    # Pass this iteration because the content of this element was extracted from the tables
                    continue

            if not is_element_inside_any_table(element, page, tables):

                # Check if the element is text element
                if isinstance(element, LTTextContainer):
                    # Use the function to extract the text and format for each text element
                    line_text, font = text_extraction(element)
                    fonts.append(font)
                    
                    text_element = TextElement(line_text, font)

                    # Добавляем в содержание страницы текстовый объект
                    page_content.append(text_element)


                # Check the elements for images
                if isinstance(element, LTFigure):
                    # Crop the image from PDF
                    crop_image(element, pageObj)
                    # Convert the croped pdf to image
                    convert_to_images(TEMP_PDF_IMAGE)
                    # Extract the text from image
                    image_text = image_to_text(TEMP_IMAGE)

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
        content_per_page.append(page_content)


    # Закрываем объект файла pdf
    pdfFileObj.close()

    # Удаляем созданные дополнительные файлы
    if os.path.exists(TEMP_PDF_IMAGE):
        os.remove(TEMP_PDF_IMAGE)
    if os.path.exists(TEMP_IMAGE):
        os.remove(TEMP_IMAGE)

    return content_per_page