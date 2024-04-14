from docx import Document
from docx.shared import Pt

import os

from Classes.Font import Font
from Classes.Elements import *

from Tools.config import WORD_FILES_PATH


# Функция, которая записывает текст в файл Word
def write_to_word(content_per_page, word_path):
    doc = Document()    # Создаем документ

    # Инициализация до цикла, для того, чтобы использовался прошлый шрифт
    font = Font()
    fonts = []
    # Цикл по страницам
    for page in content_per_page:
        # Цикл по элементам
        for element in page:
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