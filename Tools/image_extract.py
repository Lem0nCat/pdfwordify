import PyPDF2   # Для считывания PDF

# Для извлечения изображений из PDF
from PIL import Image
from pdf2image import convert_from_path

import pytesseract  # Для выполнения OCR, чтобы извлекать тексты из изображений

from .config import IMAGES_PATH, TEMP_IMAGE, TEMP_PDF_IMAGE, LANG

import os


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

    # Проверка на существование директории
    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

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