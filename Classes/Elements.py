class TextElement:
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def __str__(self):
        return f"Text: '{self.text}'\nFont: {self.font}"
    
    def set_text(self, text):
        self.text = text
        
    def set_font(self, font):
        self.font = font


class ImageElement(TextElement):
    pass


    