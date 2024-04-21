import fitz  # PyMuPDF для извлечения изображений

# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure

# Собственные классы с элементами
from Classes.Elements import *  
from Classes.Font import Font

# Директория для сохранения временных изображений
from Tools.config import IMAGES_PATH, LANG

# Инструменты для извлечения
from Tools.table_extract import *
from Tools.text_extract import *
from Tools.image_extract import *


def extract_all(path_to_pdf, flavor='lattice'):
    """
    Извлекает изображения, таблицы и текст из PDF-файла.

    Args:
        path_to_pdf (str): Путь к PDF-документу.
        flavor (str, optional): Режим извлечения таблиц (lattice, stream, None). По умолчанию 'lattice'.

    Return:
        list: Список словарей, содержащие извлеченное содержимое каждой страницы.
    """
    
    # Используем fitz для извлечения изображений
    pdf_fitz = fitz.open(path_to_pdf)

    # Извлекаем таблицы из всего файла
    # Если не выбран режим извлечения, то пользователь выбрал отсутствие таблиц
    tables_in_pages = extract_table_camelot(path_to_pdf, flavor) if flavor else None

    # Создаём словарь для извлечения текста из каждого изображения
    content_per_page = []

    # Сохраняем шрифты
    fonts = []

    # Цикл по страницам
    for page_index, page in enumerate(extract_pages(path_to_pdf)):
        # Добавляем элементы страницы в общий список
        content_per_page.append(extract_page_content(pdf_fitz, page, page_index, tables_in_pages, fonts))

    # Закрываем объект файла pdf
    pdf_fitz.close()

    # Удаляем созданные дополнительные файлы
    delete_png_files(IMAGES_PATH)

    return content_per_page


def extract_page_content(pdf_fitz, page, page_index, tables_in_pages, fonts):
    """
    Извлекает и обрабатывает содержимое указанной страницы PDF-документа.

    Args:
        pdf_fitz (fitz.Document): Объект документа PDF, загруженный через fitz.
        page (pdfminer.Page): Объект страницы, для которой необходимо извлечь содержимое.
        page_index (int): Индекс текущей страницы в документе.
        tables_in_pages (list of camelot.Table): Список, содержащий объекты таблиц Camelot для каждой страницы документа.
        fonts (list of Classes.Font): Список, содержащий объекты шрифтов Font, используемых в документе.

    Returns:
        dict: Словарь с двумя ключами:
            "page_content" (list): Список содержащий элементы страницы, такие как тексты, изображения и таблицы.
            "landscape_orientation" (bool): Флаг, указывающий на альбомную ориентацию страницы.
    """
    page_content = []

    image_index = 0  # Задаем индекс для прохожения по изображениям
    images_paths = extract_images(pdf_fitz, page_index, IMAGES_PATH)

    # Получение таблиц на текущей странице
    page_tables = tables_in_pages[page_index + 1] if tables_in_pages else None

    # Индекс таблицы на странице (если -1, то таблиц нет)
    table_index = 0 if page_tables else -1

    # Получение всех элементов на странице
    page_elements = [(element.y1, element) for element in page._objs]
    # Сортировка всех элементов по мере их расположения на странице
    page_elements.sort(key=lambda a: a[0], reverse=True)

    # Цикл по компонентам на странице
    for component in page_elements:
        # Извлечение элемента макета страницы
        element = component[1]

        # Проверка элемента на наличие таблиц
        if table_index != -1 and is_element_inside_any_table(element, page_tables):
            table_index = handle_table_element(element, page_content, page_tables, table_index)
            # Пропустить эту итерацию, потому что содержимое этого элемента было извлечено из таблиц
            continue

        handle_text_element(element, page_content, fonts)

        image_index = handle_image_element(element, page_content, fonts, images_paths, image_index)

    # Возвращаем словарь из списка элементов страницы, и альбомная ориентация или нет
    return {
        "page_content": page_content,
        "landscape_orientation": is_landscape_orientation(pdf_fitz[page_index])
    }


def handle_table_element(element, page_content, page_tables, table_index):
    """
    Обрабатывает табличный элемент на странице PDF, добавляя таблицу в содержимое страницы, если элемент соответствует текущему индексу таблицы.
    
    Args:
        element (pdfminer.layout.LTTextContainer): Элемент страницы, который может содержать таблицу.
        page_content (list): Список, в который добавляются обработанные элементы страницы.
        page_tables (list of camelot.Table): Список таблиц Camelot, полученных для страницы.
        table_index (int): Текущий индекс обрабатываемой таблицы в списке таблиц.
    
    Returns:
        int: Обновленный индекс таблицы, который указывает на следующую таблицу для обработки на странице.
    """
    table_found_index = get_table_index(element, page_tables)
    if table_found_index == table_index:
        page_content.append(page_tables[table_index])
        table_index += 1
    return table_index

# Метод для обработки текстового элемента
def handle_text_element(element, page_content, fonts):
    """
    Обрабатывает текстовый элемент страницы PDF, извлекая текст и шрифт, и добавляет результат в содержание страницы.

    Args:
        element (pdfminer.layout.LTTextContainer): Элемент страницы, который может содержать текст.
        page_content (list): Список, в который добавляются обработанные элементы страницы.
        fonts (list of Classes.Font): Список, в который добавляются шрифты используемые в текстовых элементах.
    """
    if isinstance(element, LTTextContainer):
        # Используем функцию для извлечения текста и шрифта из элемента
        line_text, font = text_extraction(element)
        fonts.append(font)

        text_element = TextElement(line_text, font)

        # Добавляем в содержание страницы объект текстового элемента
        page_content.append(text_element)

# Метод для обработки элемента с изображением
def handle_image_element(element, page_content, fonts, images_paths, image_index):
    """
    Обрабатывает элемент страницы, представляющий изображение, и извлекает текст из него.

    Args:
        element (pdfminer.layout.LTFigure): Элемент страницы, который может содержать изображение.
        page_content (list): Список, в который добавляются обработанные элементы страницы.
        fonts (list of Classes.Font): Список, в который добавляются шрифты используемые в текстовых элементах.
        images_paths (list): Список путей к изображениям, из которых нужно извлечь текст.
        image_index (int): Индекс текущего обрабатываемого изображения в списке путей.

    Returns:
        int: Обновленный индекс изображения после обработки текущего элемента.
    """
    if isinstance(element, LTFigure):
        # Извлечение текста из изображения
        image_text = image_to_text(images_paths[image_index], LANG)
        image_index += 1

        font = Font.get_default_font(fonts)

        image_element = ImageElement(image_text, font)
        page_content.append(image_element)
    
    return image_index

def is_landscape_orientation(page_object):
    """
    Определяет, является ли ориентация страницы альбомной.

    Args:
        page_object (fitz.Page): Объект страницы PDF, для которой проверяется ориентация.

    Returns:
        bool: Возвращает True, если ориентация страницы альбомная, иначе False.
    """
    return page_object.rect.width > page_object.rect.height
