from collections import Counter
from multipledispatch import dispatch
import re

class Font:
    """Класс, представляющий шрифт с различными атрибутами, такими как имя, размер, жирность и курсив."""
    def __init__(self, name='Arial', font_size=12, bold=False, italic=False):
        """
        Инициализирует объект Font с заданными значениями или значениями по умолчанию.

        Параметры:
            name (str): Название шрифта.
            font_size (int): Размер шрифта.
            bold (bool): Жирный шрифт если True.
            italic (bool): Курсивный шрифт если True.
        """
        self.name = name
        self.bold = bold
        self.italic = italic
        self.size = font_size

    def __str__(self):
        """Возвращает строковое представление объекта Font."""
        bold_status = "bold" if self.bold else "not bold"
        italic_status = "italic" if self.italic else "not italic"
        return (f"Font: {self.name}, Size: {self.size}, {bold_status}, {italic_status}")

    def set_raw_name(self, font):
        """
        Устанавливает имя шрифта, а также его жирность и курсив, анализируя строку.

        Параметры:
            font (str): Строка с названием шрифта и стилем.
        """
        clean_name, bold, italic = self.parse_font_info(font)
        self.name = clean_name
        self.bold = bold
        self.italic = italic
        
    def set_name(self, name):
        """
        Устанавливает название шрифта.

        Параметры:
            name (str): Новое название шрифта.
        """
        self.name = name
        
    def fix_current_name(self):
        """
        Обновляет текущее название шрифта, анализируя его и обновляя жирность и курсив.

        Возвращает:
            self: Возвращает сам объект для поддержки вызовов методов в цепочке.
        """
        self.name, self.bold, self.italic = self.parse_font_info(self.name)
        return self  # Возврат экземпляра для поддержки цепочек вызовов

    def set_size(self, size):
        """
        Устанавливает размер шрифта, проверяя, чтобы значение было положительным.

        Параметры:
            size (int): Новый размер шрифта.
        
        Исключения:
            ValueError: Если размер шрифта не является положительным числом.
        """
        if size > 0:
            self.size = size
        else:
            raise ValueError("Font size must be positive")

    def toggle_bold(self):
        """Переключает жирность шрифта."""
        self.bold = not self.bold

    def toggle_italic(self):
        """Переключает курсив шрифта."""
        self.italic = not self.italic

    
    @staticmethod
    def parse_font_info(font_name):
        """
        Парсит строку с названием шрифта, извлекая из неё название, жирность и курсив.

        Параметры:
            font_name (str): Строка с названием шрифта и стилем.

        Возвращает:
            tuple: Возвращает кортеж с названием шрифта, жирностью и курсивом.
        """
        parts = font_name.split('+')
        style_info = parts[-1] if parts else ''
        clean_name_parts = re.split(',|-|;|_', style_info)
        clean_name = clean_name_parts[0]

        bold = 'Bold' in style_info
        italic = 'Italic' in style_info

        return clean_name, bold, italic
    
    @dispatch(list, list)
    @staticmethod
    def get_default_font(fonts, sizes):
        """
        Определяет наиболее часто используемый шрифт и размер из списков названий и размеров.

        Параметры:
            fonts (list of str): Список названий шрифтов.
            sizes (list of float): Список размеров шрифтов.

        Возвращает:
            Font: Объект шрифта с наиболее часто используемыми значениями.
        """
        font = Font()
        if (fonts):
            # Подсчитываем встречаемость каждого шрифта и размера
            name_counter = Counter(fonts)
            # Находим самый частый шрифт и размер
            most_common_name = name_counter.most_common(1)[0][0]
            font.set_name(most_common_name)
            
        if (sizes):
            size_counter = Counter(sizes)
            most_common_size = size_counter.most_common(1)[0][0]
            font.set_size(most_common_size)

        return font
    
    @dispatch(list)
    @staticmethod
    def get_default_font(font_list):
        """
        Определяет наиболее часто используемый шрифт и размер из списка объектов Font.

        Параметры:
            font_list (list of Font): Список объектов Font.

        Возвращает:
            Font: Объект шрифта с наиболее часто используемыми значениями.
        """
        font = Font()
        if (font_list):
            # Подсчитываем встречаемость каждого атрибута шрифта
            font_names = [font.name for font in font_list]
            font_sizes = [font.size for font in font_list]

            # С помощью Counter находим самые частые значения для каждого атрибута
            most_common_name = Counter(font_names).most_common(1)[0][0]
            most_common_size = Counter(font_sizes).most_common(1)[0][0]
            
            font.set_name(most_common_name)
            font.set_size(most_common_size)

        return font
