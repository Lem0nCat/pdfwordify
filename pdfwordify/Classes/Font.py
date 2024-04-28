from collections import Counter
from multipledispatch import dispatch
import re

class Font:
    """A class representing a font with various attributes such as name, size, boldness and italics."""""
    def __init__(self, name='Arial', font_size=12, bold=False, italic=False):
        """
        Initializes the Font object with the given values or default values.

        Parameters:
            name (str): The name of the font.
            font_size (int): The size of the font.
            bold (bool): Bold font if True.
            italic (bool): Italic font if True.
        """
        self.name = name
        self.bold = bold
        self.italic = italic
        self.size = font_size

    def __str__(self):
        """Returns a string representation of the Font object."""
        bold_status = "bold" if self.bold else "not bold"
        italic_status = "italic" if self.italic else "not italic"
        return (f"Font: {self.name}, Size: {self.size}, {bold_status}, {italic_status}")

    def set_raw_name(self, font):
        """
        Sets the font name, as well as its boldness and italics, by analyzing the string.

        Parameters:
            font (str): A string with the font name and style.
        """
        clean_name, bold, italic = self.parse_font_info(font)
        self.name = clean_name
        self.bold = bold
        self.italic = italic
        
    def set_name(self, name):
        """
        Sets the name of the font.

        Parameters:
            name (str): The new name of the font.
        """
        self.name = name
        
    def fix_current_name(self):
        """
        Updates the current font name by analyzing it and updating the boldness and italics.

        Returns:
            self: Returns the object itself to support method calls in the chain.
        """
        self.name, self.bold, self.italic = self.parse_font_info(self.name)
        return self  # Return an instance to support call chains

    def set_size(self, size):
        """
        Sets the font size, checking that the value is positive.

        Parameters:
            size (int): The new font size.
        
        Exceptions:
            ValueError: If the font size is not a positive number.
        """
        if size > 0:
            self.size = size
        else:
            raise ValueError("Font size must be positive")

    def toggle_bold(self):
        """Switches the boldness of the font."""
        self.bold = not self.bold

    def toggle_italic(self):
        """Toggles the italicized font."""
        self.italic = not self.italic

    
    @staticmethod
    def parse_font_info(font_name):
        """
        Parses the font name string, extracting the font name, boldness and italics from it.

        Parameters:
            font_name (str): A string with the font name and style.

        Returns:
            tuple: Returns a tuple with the font name, boldness, and italics.
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
        Determines the most commonly used font and size from the lists of names and sizes.

        Parameters:
            fonts (list of str): A list of font names.
            sizes (list of float): A list of font sizes.

        Returns:
            Font: A font object with the most commonly used values.
        """
        font = Font()
        if (fonts):
            # Count the occurrence of each font and size
            name_counter = Counter(fonts)
            # Find the most common font and size
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
        Determines the most frequently used font and size from the font list.

        Parameters:
            font_list (list of Font): A list of Font objects.

        Returns:
            Font: Font object with the most frequently used values.
        """
        font = Font()
        if (font_list):
            # Count the occurrence of each font attribute
            font_names = [font.name for font in font_list]
            font_sizes = [font.size for font in font_list]

            # Use Counter to find the most frequent values for each attribute
            most_common_name = Counter(font_names).most_common(1)[0][0]
            most_common_size = Counter(font_sizes).most_common(1)[0][0]
            
            font.set_name(most_common_name)
            font.set_size(most_common_size)

        return font
