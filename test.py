import PyPDF2   # Для считывания PDF

# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure

import pdfplumber   # Для извлечения текста из таблиц в PDF

# Для извлечения изображений из PDF
from PIL import Image
from pdf2image import convert_from_path

import pytesseract  # Для выполнения OCR, чтобы извлекать тексты из изображений

import os   # Для удаления дополнительно созданных файлов


# Функция извлекает текст из текстового элемента
# и добавляет информацию о размере и стиле шрифта
def text_extraction(element):
    # Извлекаем текст
    line_text = element.get_text()

    # Находим форматы текста
    # Инициализируем список со всеми форматами, встречающимися в строке текста
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Итеративно обходим каждый символ в строке текста
            for character in text_line:
                if isinstance(character, LTChar):
                    # Добавляем к символу название шрифта
                    line_formats.append(character.fontname)
                    # Добавляем к символу размер шрифта
                    line_formats.append(character.size)
    # Находим уникальные размеры и названия шрифтов в строке
    format_per_line = list(set(line_formats))

    # Возвращаем кортеж с текстом в каждой строке вместе с его форматом
    return (line_text, format_per_line)


# Функция извлечения изображений из PDF
def crop_image(element, pageObj):
    # Получаем координаты для вырезания изображения из PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1]

    # Обрезаем страницу по координатам (left, bottom, right, top)
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)

    # Сохраняем обрезанную страницу в новый PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)

    # Сохраняем обрезанный PDF в новый файл
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Создаём функцию для преобразования PDF в изображения
def convert_to_images(input_file,):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_image.png"
    image.save(output_file, "PNG")

# Создаём функцию для считывания текста из изображений
def image_to_text(image_path):
    # Считываем изображение
    img = Image.open(image_path)
    # Извлекаем текст из изображения
    text = pytesseract.image_to_string(img, lang="rus+eng")
    return text


# Извлечение таблиц из страницы

# Извлекает указанную в параметрах таблицу из файла
def extract_table(pdf_path, page_num, table_num):
    # Открываем файл PDF
    pdf = pdfplumber.open(pdf_path)
    # Находим исследуемую страницу
    table_page = pdf.pages[page_num]
    # Извлекаем соответствующую таблицу
    table = table_page.extract_table()[table_num]
    return table

# Преобразуем таблицу в читабельный строковый формат
def table_converter(table):
    table_string = ''

    # Интеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        # Удаляем разрыв строки из текста с переносом
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        # Преобразуем



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
for page_num, page in enumerate(extract_pages("/home/gitler/Desktop/diplom/Resources/PDF_files/test.pdf")):

    # Итеративно обходим элементы, из которых состоит страница
    for element in page:

        # Проверяем, является ли элемент текстовым
        if isinstance(element, LTTextContainer):
            # print(text_extraction(element))
            # Функция для извлечения текста из текстового блока
            pass

            # Функция для извлечения формата текста
            pass

        # Проверка элементов на наличие изображений
        if isinstance(element, LTFigure):
            # Функция для преобразования PDF в изображение
            pass

            # Функция для извлечения текста при помощи OCR 
            pass

        # Проверка элементов на наличие таблиц
        if isinstance(element, LTRect):
            # Функция для извлечения таблицы
            pass
            # Функция для преобразования содержимого таблицы в строку
            pass


print(image_to_text("/home/gitler/Desktop/diplom/Resources/PDF_files/PDF_image.png"))


