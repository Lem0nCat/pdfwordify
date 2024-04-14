import pdfplumber   # Для извлечения текста из таблиц в PDF

from Tools.config import TABLE_SETTINGS


# # # # # # # # # # # # # # # # # # # # #
# #   Извлечение текста из таблиц   # # #
# # # # # # # # # # # # # # # # # # # # #

# Извлекает указанную в параметрах таблицу из файла
def extract_table(pdf_path, page_index, table_index):
    # Открываем файл PDF
    pdf = pdfplumber.open(pdf_path)
    # Находим исследуемую страницу
    table_page = pdf.pages[page_index]
    # Извлекаем соответствующую таблицу
    table = table_page.extract_tables(table_settings=TABLE_SETTINGS)[table_index]
    return table

# Create a function to check if the element is in any tables present in the page
def is_element_inside_any_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

# Function to find the table for a given element
def find_table_for_element(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i  # Return the index of the table
    return None  