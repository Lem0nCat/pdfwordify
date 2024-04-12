from collections import Counter
from multipledispatch import dispatch

class Font:
    def __init__(self, name='Arial', font_size=12, bold=False, italic=False):
        self.name = name
        self.bold = bold
        self.italic = italic
        self.size = font_size

    def __str__(self):
        # Возвращаем строковое представление объекта класса
        bold_status = "bold" if self.bold else "not bold"
        italic_status = "italic" if self.italic else "not italic"
        return (f"Font: {self.name}, Size: {self.size}, {bold_status}, {italic_status}")

    def set_raw_name(self, font):
        # Парсинг информации о шрифте и обновление свойств
        clean_name, bold, italic = self.parse_font_info(font)
        self.name = clean_name
        self.bold = bold
        self.italic = italic
        
    def set_name(self, name):
        self.name = name
        
    def fix_current_name(self):
        self.name, self.bold, self.italic = self.parse_font_info(self.name)
        return self  # Возврат экземпляра для поддержки цепочек вызовов

    def set_size(self, size):
        if size > 0:
            self.size = size
        else:
            raise ValueError("Font size must be positive")

    def toggle_bold(self):
        self.bold = not self.bold

    def toggle_italic(self):
        self.italic = not self.italic


    @staticmethod
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
    @dispatch(list, list)
    @staticmethod
    def get_default_font(fonts, sizes):
        # Подсчитываем встречаемость каждого шрифта и размера
        name_counter = Counter(fonts)
        size_counter = Counter(sizes)

        # Находим самый частый шрифт и размер
        most_common_name = name_counter.most_common(1)[0][0]
        most_common_size = size_counter.most_common(1)[0][0]

        return Font(most_common_name, most_common_size)
    
    @dispatch(list)
    @staticmethod
    def get_default_font(font_list):
        # Подсчитываем встречаемость каждого атрибута шрифта
        font_names = [font.name for font in font_list]
        font_sizes = [font.size for font in font_list]

        # С помощью Counter находим самые частые значения для каждого атрибута
        most_common_name = Counter(font_names).most_common(1)[0][0]
        most_common_size = Counter(font_sizes).most_common(1)[0][0]

        # Создаем и возвращаем экземпляр Font с самыми частыми значениями
        return Font(most_common_name, most_common_size)