from pdfminer.layout import LTTextContainer, LTChar

from Classes.Font import Font

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
                cleaned_texts.append(line + ' ')
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