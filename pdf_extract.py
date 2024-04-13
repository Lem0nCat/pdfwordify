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

from collections import Counter # Для подсчета часто используемого шрифта и размера текста

from Elements import * # Собственные классы с элементами
from Font import Font

# Пути для временных файлов
TEMP_PDF_IMAGE = "Resources/Images/cropped_image.pdf"
TEMP_IMAGE = "Resources/Images/PDF_image.png"

# Язык для GOOGLE TESSERACT OCR
LANG = "rus+eng"


# # # # # # # # # # # # # # # # # # #
# #   Извлечение текста из PDF  # # #
# # # # # # # # # # # # # # # # # # #

def text_extraction(element):
    # Извлекаем текст из элемента, предполагая, что он текстовый контейнер
    line_texts = element.get_text().split('\n') if isinstance(element, LTTextContainer) else [""]
    
    # Очищаем текст, удаляя ненужные переносы строк внутри абзацев
    cleaned_texts = []
    for i, line in enumerate(line_texts):
        if (i < len(line_texts) - 1):
            next_line = line_texts[i + 1].strip()
            if (next_line and next_line[0].isalpha()):
                cleaned_texts.append(line)
            else:
                cleaned_texts.append(line + '\n')
        else:
            pass
    
    cleaned_text = ''.join(cleaned_texts)
    
    # Сбор информации о шрифтах
    fonts, sizes = [], []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    # Сохраняем имя и размер шрифта первого символа в строке и прекращаем цикл
                    fonts.append(character.fontname)
                    sizes.append(round(character.size, 1))
                    break  # Прерываем цикл после получения шрифта
    
    font = Font.get_default_font(fonts, sizes).fix_current_name()
    
    # Возвращаем текст и самый частый шрифт
    return cleaned_text, font


# # # # # # # # # # # # # # # # # # # # #
# #   Извлечение текста из таблиц   # # #
# # # # # # # # # # # # # # # # # # # # #

# Извлекает указанную в параметрах таблицу из файла
def extract_table(pdf_path, page_index, table_index):
    # Открываем файл PDF
    pdf = pdfplumber.open(pdf_path)
    # Находим исследуемую страницу
    table_page = pdf.pages[page_index]
    # Извлекаем соответствующую таблицу
    table = table_page.extract_tables()[table_index]
    return table

# Create a function to check if the element is in any tables present in the page
def is_element_inside_any_table(element, page ,tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

# Function to find the table for a given element
def find_table_for_element(element, page ,tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i  # Return the index of the table
    return None  


# # # # # # # # # # # # # # # # # # # # # # # 
# #   Извлечение текста из изображений  # # #
# # # # # # # # # # # # # # # # # # # # # # # 

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
    with open(TEMP_PDF_IMAGE, 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Функция для преобразования PDF в изображения
def convert_to_images(input_file,):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = TEMP_IMAGE
    image.save(output_file, "PNG")

# Функция для считывания текста из изображений
def image_to_text(image_path):
    img = Image.open(image_path)
    # Извлекаем текст из изображения
    text = pytesseract.image_to_string(img, lang=LANG)
    return text


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
        
        # Количество исследуемых таблиц на старнице
        table_in_page = -1
        # Открытие pdf файла
        pdf = pdfplumber.open(path_to_pdf)
        # Текущая страница
        page_tables = pdf.pages[pagenum]
        # Нахождение таблиц на странице
        tables = page_tables.find_tables()
        
        if len(tables) != 0:
            table_in_page = 0

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
            if table_in_page == -1:
                pass
            else:
                if is_element_inside_any_table(element, page, tables):
                    table_found = find_table_for_element(element,page ,tables)
                    if table_found == table_in_page and table_found != None:   
                        table = TableElement(extracted_tables[table_in_page])
                         
                        page_content.append(table)
                        table_in_page += 1
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