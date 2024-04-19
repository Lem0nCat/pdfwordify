# Для извлечения изображений из PDF
from PIL import Image

import fitz # PyMuPDF

import pytesseract  # Для выполнения OCR, чтобы извлекать тексты из изображений

from .config import IMAGES_PATH, LANG


# # # # # # # # # # # # # # # # # # # # # # # 
# #   Извлечение текста из изображений  # # #
# # # # # # # # # # # # # # # # # # # # # # # 

def extract_images(document, page_index):
    page = document.load_page(page_index)   # Загрузка страницы
    # Извлечение изображений со страницы
    image_list = page.get_images(full=True)
    image_paths = []    # Пути извлеченных изображений
    
    # Сохранение каждого изображения со страницы
    for image_index, img in enumerate(image_list):
        xref = img[0]   # XREF изображения
        base_image = document.extract_image(xref)
        image_bytes = base_image['image']   # Извлечение самих данных изображения
        
        # Создание пути для изображения
        image_path = IMAGES_PATH + f'/image_{page_index+1}_{image_index+1}.png'
        
        # Запись изображения в файл
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        image_paths.append(image_path)
        
    return image_paths

# Функция для считывания текста из изображений
def image_to_text(image_path):
    img = Image.open(image_path)
    # Извлекаем текст из изображения
    text = pytesseract.image_to_string(img, lang=LANG)
    return text

# Класс для работы Camelot
class ConversionBackend(object):
    def convert(self, pdf_path, png_path):
        # Открываем документ
        doc = fitz.open(pdf_path) 
        for page in doc.pages():
            # Переводим страницу в картинку
            pix = page.get_pixmap()  
            # Сохраняем
            pix.save(png_path)