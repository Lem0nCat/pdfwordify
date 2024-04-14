from docx import Document
from docx.shared import Pt, Inches
from docx.enum.section import WD_ORIENT

import os

from Classes.Font import Font
from Classes.Elements import *

from Tools.config import WORD_FILES_PATH


def set_orientation(section, is_landscape):
    """
    Создает новый раздел с заданной ориентацией.

    Args:
    section: Объект секции docx.
    is_landscape: Булево значение, True если нужна альбомная ориентация, иначе False.
    """
    
    if is_landscape:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Inches(11)
        section.page_height = Inches(8.5)
    else:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)


# Функция, которая записывает текст в файл Word
def write_to_word(content_per_page, word_path):
    doc = Document()    # Создаем документ
            
    first_page = True

    # Инициализация до цикла, для того, чтобы использовался прошлый шрифт
    font = Font()
    fonts = []
    # Цикл по страницам
    for page in content_per_page:   
        # При создании документа создается секция, которую мы получаем
        if first_page:
            section = doc.sections[0]  # Используем первый существующий раздел
            first_page = False
        else:
            section = doc.add_section()  # Создаем новый раздел для следующих страниц
            
        # Изменение ориентации страницы, если альбомная
        set_orientation(section, page['landscape_orientation'])
        
        # Цикл по элементам
        for element in page['page_content']:
            # Если элемент существует и он является либо текстовым, либо изображением
            if element and (isinstance(element, TextElement) or isinstance(element, ImageElement)):
                # Проверка на пустое содержание текста
                if (element.text.lower().strip() != ""):
                    # Создаем элемент параграфа
                    paragraph = doc.add_paragraph()
                    
                    # Создаем элемент Run с текстом
                    run = paragraph.add_run(element.text)
                    
                    font = element.font
                    # Меняем стили текста
                    if (font):                      
                        run.font.name = font.name
                        run.font.size = Pt(font.size)
                        run.font.bold = font.bold
                        run.font.italic = font.italic
                        
                        fonts.append(font)
                        
            # Если элемент существует и он является табличным
            elif element and isinstance(element, TableElement):
                # Добавляем пустую таблицу 
                table = doc.add_table(rows=element.num_rows, cols=element.num_cols)
                
                # добавляем данные к существующей таблице
                for i, row in enumerate(element.data):
                    # Получаем ячейки строки в таблице
                    row_cells = table.rows[i].cells
                    for j, item in enumerate(row):
                        paragraph = row_cells[j].paragraphs[0]
                        run = paragraph.add_run(item)
                        
                        # Меняем стили текста
                        if (len(fonts) > 2):
                            font = Font.get_default_font(fonts)
                                                  
                        run.font.name = font.name
                        run.font.size = Pt(font.size) if font.size <= 10 else Pt(10.0)
                    
    # Проверка на существование директории
    if not os.path.exists(WORD_FILES_PATH):
        os.makedirs(WORD_FILES_PATH)
        
    doc.save(word_path)
    print(f"Документ успешно сохранен ({word_path})")