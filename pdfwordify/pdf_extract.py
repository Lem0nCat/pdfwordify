import fitz  # PyMuPDF for image extraction

# To analyze PDF structure and extract text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure

# Own classes with elements
from pdfwordify.Classes.Elements import *  
from pdfwordify.Classes.Font import Font

# Extraction tools
from pdfwordify.Tools.table_extract import *
from pdfwordify.Tools.text_extract import *
from pdfwordify.Tools.image_extract import *


def extract_all(path_to_pdf, flavor='lattice', ocr_text_lang='eng'):
    """
    Extracts images, tables and text from a PDF file.

    Args:
        path_to_pdf (str): The path to the PDF document.
        flavor (str, optional): Table extraction mode (lattice, stream, None). The default is 'lattice'.
        ocr_text_lang (str, optional): Language for Google Tesseract OCR. Defaults to 'eng'.

    Return:
        list: List of dictionaries containing the extracted content of each page.
    """
    
    # Create a dictionary to extract text from each image
    content_per_page = []
    # Save the fonts
    fonts = []
    
    pdf_fitz = None
    try:
        # Use fitz to extract images
        pdf_fitz = fitz.open(path_to_pdf)
        
        # Extract tables from the entire file
        # If extract mode is not selected, the user has selected no tables
        tables_in_pages = extract_table_camelot(path_to_pdf, flavor) if flavor else None

        # Cycle through the pages
        for page_index, page in enumerate(extract_pages(path_to_pdf)):
            # Add page elements to the shared list
            content_per_page.append(extract_page_content(pdf_fitz, page, page_index, tables_in_pages, fonts, ocr_text_lang))
    
    except Exception as e:
        raise Exception(f"An error occurred while processing the PDF file: {path_to_pdf}") from e
    finally:
        if pdf_fitz:
            pdf_fitz.close()

    return content_per_page


def extract_page_content(pdf_fitz, page, page_index, tables_in_pages, fonts, ocr_text_lang='eng'):
    """
    Extracts and processes the contents of the specified page of a PDF document.

    Args:
        pdf_fitz (fitz.Document): The object of the PDF document uploaded via fitz.
        page (pdfminer.Page): The object of the page for which the content is to be extracted.
        page_index (int): The index of the current page in the document.
        tables_in_pages (list of camelot.Table): A list containing Camelot table objects for each page in the document.
        fonts (list of Classes.Font): A list containing Font objects used in the document.
        ocr_text_lang (str, optional): The language for Google Tesseract OCR. Defaults to 'eng'.

    Returns:
        dict: A dictionary with two keys:
            "page_content" (list): A list containing page elements such as text, images, and tables.
            "landscape_orientation" (bool): Flag indicating the landscape orientation of the page.
    """
    page_content = []
    image_index = 0  # Set the index for traversing images
    
    try:
        # Extract images from the current page
        temp_images = extract_images(pdf_fitz, page_index)

        # Retrieve tables on the current page
        page_tables = tables_in_pages[page_index + 1] if tables_in_pages else None

        # Table index on the page (if -1, there are no tables)
        table_index = 0 if page_tables else -1

        # Get all the elements on the page
        page_elements = [(element.y1, element) for element in page._objs]
        # Sort all elements as they appear on the page
        page_elements.sort(key=lambda a: a[0], reverse=True)

        # Cycle through the components on the page
        for component in page_elements:
            # Retrieve a page layout element
            element = component[1]

            # Check the item for tables
            if table_index != -1 and is_element_inside_any_table(element, page_tables):
                table, table_index = handle_table_element(element, page_tables, table_index)
                if table: page_content.append(table)
                # Skip this iteration because the contents of this item have been extracted from the tables
                continue

            # Processing of a text element, if any
            text_element = handle_text_element(element, fonts)
            if text_element: page_content.append(text_element)

            # Processing of an image element, if any
            image_element, image_index = handle_image_element(element, fonts, temp_images, image_index, ocr_text_lang)
            if image_element: page_content.append(image_element)
        
        # Close temporary files and delete
        finalize_temp_images(temp_images)
    
    except Exception as e:
        raise Exception(f"An error occurred while processing page {page_index} of the PDF.") from e

    # Return the dictionary from the list of page elements, and landscape orientation flag
    return {
        "page_content": page_content,
        "landscape_orientation": is_landscape_orientation(pdf_fitz[page_index])
    }


def handle_table_element(element, page_tables, table_index):
    """
    Processes a table element on a PDF page, returning a table if the element matches the current table index.
    
    Args:
        element (pdfminer.layout.LTTextContainer): A page element that can contain a table.
        page_tables (list of camelot.Table): A list of Camelot tables retrieved for the page.
        table_index (int): The current index of the processed table in the list of tables.
    
    Returns:
        tuple: A tuple containing the next table (camelot.Table) and the updated index if a match is found, 
               or None and the current index if no match is found.
    """
    table_found_index = get_table_index(element, page_tables)
    if table_found_index == table_index:
        return page_tables[table_index], table_index + 1
    return None, table_index

def handle_text_element(element, fonts):
    """
    Processes the text element of a PDF page, extracting the text and font, returning an image element

    Args:
        element (pdfminer.layout.LTTextContainer): A page element that can contain an image.
        fonts (list of Classes.Font): List to which fonts used in text elements are added.
    
    Returns:
        pdfwordify.Classes.Elements.TextElement: Returns the text element object or None if the element does not contain a text element.
    """
    if isinstance(element, LTTextContainer):
        # Use the function to extract text and font from the element
        line_text, font = text_extraction(element)
        fonts.append(font)

        text_element = TextElement(line_text, font)

        # Return the text element
        return text_element
    return None

def handle_image_element(element, fonts, temp_images, image_index, ocr_text_lang='eng'):
    """
    Processes the page element representing the image and extracts the text from it.

    Args:
        element (pdfminer.layout.LTFigure): A page element that can contain an image.
        fonts (list of Classes.Font): A list of fonts, to find a frequently used one.
        temp_images (list): List of temporary images extracted from this page.
        image_index (int): The index of the currently processed image in the path list.
        ocr_text_lang (str, optional): Language for Google Tesseract OCR. Defaults to 'eng'.

    Returns:
        tuple: Returns a tuple that consists of an object (pdfwordify.Classes.Elements.ImageElement) and an updated index,
               or None and the previous index if the element contains no images.
    """
    if isinstance(element, LTFigure):
        # Extract text from an image
        image_text = image_to_text(temp_images[image_index], ocr_text_lang)

        font = Font.get_default_font(fonts)

        image_element = ImageElement(image_text, font)
        return image_element, image_index + 1
    return None, image_index

def is_landscape_orientation(page_object):
    """
    Determines whether the page orientation is landscape.

    Args:
        page_object (fitz.Page): The PDF page object for which the orientation is checked.

    Returns:
        bool: Returns True if the page orientation is landscape, otherwise False.
    """
    return page_object.rect.width > page_object.rect.height
