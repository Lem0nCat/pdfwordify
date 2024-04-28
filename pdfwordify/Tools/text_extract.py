from pdfminer.layout import LTTextContainer, LTChar

from pdfwordify.Classes.Font import Font


def text_extraction(element):
    """
    Extracts text from an element.
    
    Args:
        element (pdfminer.layout.LTTextContainer): The text container of the PDF document page.
        
    Returns:
        str: The cleared text that was extracted from the container.
        Classes.Font: The font that was more commonly used in the container. 
    """
    line_texts = element.get_text().split('\n') if isinstance(element, LTTextContainer) else [""]
    
    # Clean up the text by removing unnecessary line breaks within paragraphs
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
    
    # Collect font information
    fonts, sizes = [], []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    # Save the name and font size of the first character in the string and terminate the loop
                    fonts.append(character.fontname)
                    sizes.append(round(character.size, 1))
                    break  # Break the loop when the font is received
    
    font = Font.get_default_font(fonts, sizes).fix_current_name()
    
    # Return the text and the most frequent font
    return cleaned_text, font
