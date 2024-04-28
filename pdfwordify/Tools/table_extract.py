import camelot  # To extract text from tables to PDF
from collections import defaultdict

import math

from pdfwordify.Tools.image_extract import ConversionBackend


def extract_table_camelot(pdf_path, flavor='lattice'):  
    """
    Extracts all tables from a PDF document.
    
    Args:
        pdf_path: The path to the PDF document.
        flavor (str, optional): Table extraction mode (lattice, stream, None). The default is 'lattice'.
        
    Returns:
        defaultdict of camelot.core.Table: List of all extracted tables from the document, which are grouped by page.
    """
    # Settings for table extraction
    args = {
        'backend': ConversionBackend(),
        'pages': 'all',
        'flavor': flavor
    }
    
    # Add arguments that depend on the lattice value
    if flavor == 'lattice':
        args['line_scale'] = 30

    # Call a function with dynamically generated arguments
    tables = camelot.read_pdf(pdf_path, **args)
    
    # Group tables by page
    page_tables = defaultdict(list)
    for table in tables:
        page_tables[table.page].append(table)
    return page_tables


def normalize_table_coordinates(table):
    """
    Roughs up the coordinates of the table.
    
    Args: 
        table (camelot.core.Table): Camelot table.
    
    Returns:
        (int, int, int, int, int, int): The coordinates of the table.
    """
    x0, y0, x1, y1 = table._bbox
    x0, y0 = math.floor(x0), math.floor(y0)
    x1, y1 = math.ceil(x1), math.ceil(y1)
    return x0, y0, x1, y1

def get_table_index(element, tables):
    """
    Determines the index of the table that contains a given element within a PDF document.

    Args:
        element (pdfminer.layout.LTItem): An element within a PDF page, typically representing textual or graphical data.
            The element must have a bounding box attribute ('bbox') defined as (x0, y0, x1, y1).
        tables (list of camelot.core.Table): List of table objects, each potentially containing multiple elements of a PDF page.
            Each table object must have a '_bbox' attribute defined similarly to element's 'bbox'.

    Returns:
        int or None: The zero-based index of the table that contains the element. Returns None if the element is not contained in any table.
    """
    x0, y0, x1, y1 = element.bbox

    for i, table in enumerate(tables):
        table_x0, table_y0, table_x1, table_y1 = table._bbox
        if (x0 >= table_x0 and x1 <= table_x1) and (y0 >= table_y0 and y1 <= table_y1):
            return i  # Return the table index
    return None

def is_element_inside_any_table(element, tables):
    """
    Checking for the presence of an item in some table
    
    Args:
        element (pdfminer.layout): An element within a page of a PDF document.
        tables (list of camelot.core.TableList): A list of objects of the camelot table class.
    
    Returns:
        bool: Returns True if the element is contained in one of the tables.
    """
    x0, y0, x1, y1 = element.bbox

    for table in tables:
        table_x0, table_y0, table_x1, table_y1 = normalize_table_coordinates(table)
        if (x0 >= table_x0 and x1 <= table_x1) and (y0 >= table_y0 and y1 <= table_y1):
            return True  # Return 'True' if the table was found
    return False
