class TextElement:
    """Класс для представления текстового элемента с настраиваемым текстом и шрифтом."""
    def __init__(self, text, font):
        """
        Инициализирует TextElement с заданным текстом и шрифтом.

        Параметры:
            text (str): Текст элемента.
            font (str): Шрифт текста.
        """
        self.text = text
        self.font = font

    def __str__(self):
        """Возвращает строковое представление объекта TextElement."""
        return f"Text: '{self.text}'\nFont: {self.font}"
    
    def set_text(self, text):
        """
        Устанавливает текст элемента.

        Параметры:
            text (str): Новый текст элемента.
        """
        self.text = text
        
    def set_font(self, font):
        """
        Устанавливает шрифт элемента.

        Параметры:
            font (str): Новый шрифт элемента.
        """
        self.font = font


class ImageElement(TextElement):
    """
    Класс для представления элемента изображения.
    Наследует все свойства и методы TextElement без изменений для лучшего представления, что за элемент.
    """
    pass
    