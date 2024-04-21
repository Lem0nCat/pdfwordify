from PIL import Image   # Для открытия изображения

import fitz # PyMuPDF для извлечения изображений из PDF

import pytesseract  # Для выполнения OCR, чтобы извлекать тексты из изображений

import os # Для удаления дополнительно созданных файлов


# # # # # # # # # # # # # # # # # # # # # # # 
# #   Извлечение текста из изображений  # # #
# # # # # # # # # # # # # # # # # # # # # # # 

def extract_images(document, page_index, images_path):
    """
    Извлекает все изображения с указанной страницы документа PDF и сохраняет их в заданный путь.
    
    Args:
        document (fitz.Document): Документ, из которого извлекаются изображения.
        page_index (int): Индекс страницы в документе.
        images_path (str): Путь к директории, куда будут сохраняться извлеченные изображения.
    
    Returns:
        list: Список путей к сохраненным файлам изображений.
    """
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
        image_path = f'{images_path}/image_{page_index+1}_{image_index+1}.png'
        
        # Запись изображения в файл
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        image_paths.append(image_path)
        
    return image_paths

def image_to_text(image_path, lang):
    """
    Преобразует файл изображения в текст с использованием оптического распознавания символов (OCR).
    
    Args:
        image_path (str): Путь к файлу изображения, который нужно преобразовать.
        lang (str): Язык текста, который нужно извлечь.
    
    Returns:
        str: Извлеченный текст из изображения.
    """
    img = Image.open(image_path)
    # Извлекаем текст из изображения
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def delete_png_files(directory):
    """Удаляет все файлы PNG в указанной директории."""
    # Перебор всех файлов в директории
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            file_path = os.path.join(directory, filename)
            # Удаление файла
            os.remove(file_path)

class ConversionBackend(object):
    """Класс для обработки конвертации страниц PDF в формат PNG."""
    def convert(self, pdf_path, png_path):
        # Открываем документ
        doc = fitz.open(pdf_path) 
        for page in doc.pages():
            # Переводим страницу в картинку
            pix = page.get_pixmap()  
            # Сохраняем
            pix.save(png_path)
