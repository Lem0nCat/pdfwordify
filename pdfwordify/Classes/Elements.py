class TextElement:
    """A class to represent a text element with customizable text and font."""
    def __init__(self, text, font):
        """
        Initializes a TextElement with the given text and font.

        Parameters:
            text (str): The text of the element.
            font (str): The font of the text.
        """
        self.text = text
        self.font = font

    def __str__(self):
        """Returns the string representation of a TextElement object."""
        return f"Text: '{self.text}'\nFont: {self.font}"
    
    def set_text(self, text):
        """
        Sets the text of the element.

        Parameters:
            text (str): The new text of the element.
        """
        self.text = text
        
    def set_font(self, font):
        """
        Sets the font of the element.

        Parameters:
            font (str): The new font of the element.
        """
        self.font = font


class ImageElement(TextElement):
    """
    A class to represent an image element.
    Inherits all TextElement properties and methods unchanged for a better representation of what the element is.
    """
    pass
