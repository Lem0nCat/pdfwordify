from docx import Document
from docx.shared import Pt
from collections import Counter


def parse_font_info(font_name):
    bold = 'Bold' in font_name.split('+')[-1]
    italic = 'Italic' in font_name.split('+')[-1]

    # Очистка имени шрифта от меток стиля
    clean_name_parts = font_name.split('+')[-1].split(',')
    clean_name = clean_name_parts[0]
    if 'Bold' in clean_name_parts:
        clean_name = clean_name.replace('Bold', '').strip()
    if 'Italic' in clean_name_parts:
        clean_name = clean_name.replace('Italic', '').strip()

    return clean_name, bold, italic

# Функция, которая находит самый часто используемый шрифт и размер
def get_default_font(elements):
    # Извлечение шрифтов и их размеров из элементов
    fonts_and_sizes = [(element[0], element[1]) for element in elements if isinstance(element, tuple)]
    
    # Подсчет частоты каждого шрифта и размера
    font_counter = Counter([font for font, _ in fonts_and_sizes])
    size_counter = Counter([size for _, size in fonts_and_sizes])
    
    # Находим самый часто используемый шрифт и размер
    most_common_font, _ = font_counter.most_common(1)[0]
    most_common_size, _ = size_counter.most_common(1)[0]
    
    return most_common_font, most_common_size

# Функция, которая записывает текст в файл Word
def write_to_word(text_per_page, word_path):
    doc = Document()    # Создаем документ

    # Инициализация до цикла, для того, чтобы использовался прошлый шрифт
    fontname, fontsize = None, None
    # Цикл по страницам
    for page in text_per_page:
        # Цикл по элементам
        for i in range(len(page['page_content'])):
            # Если элемент не пустой создаем параграф
            if (page["page_content"][i].lower().strip() != ""):
                # Создаем элемент параграфа
                paragraph = doc.add_paragraph()
                
                # Проверка на список и пустой список
                if (isinstance(page['line_format'][i], list) and len(page['line_format'][i]) > 0):
                    # Получаем часто используемое название и размер шрифта данного элемента
                    fontname, fontsize = get_default_font(page['line_format'][i])
                
                # Создаем элемент Run с текстом
                run = paragraph.add_run(page["page_content"][i])
                
                # Меняем стили текста
                if (fontname and fontsize):
                    fontname, bold, italic = parse_font_info(fontname)
                    
                    run.font.name = fontname
                    run.font.size = Pt(fontsize)
                    run.font.bold = bold
                    run.font.italic = italic
                    

    doc.save(word_path)
    print(f"Документ успешно сохранен ({word_path})")
