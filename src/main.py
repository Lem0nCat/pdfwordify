from docx import Document

from src.pdf_extract import extract_all
from src.save_word import write_to_word


FILE_NAME = "big-table"
PDF_PATH = f"Resources/PDF_files/{FILE_NAME}.pdf"
WORD_PATH = f"Resources/word_files/{FILE_NAME}.docx"

def get_tree(pages):
    for i, page in enumerate(pages):
        print(f'Page #{i}')
        for j, element in enumerate(page):
            print(f'\tElement #{j}')
            
            print(f'\t\t{type(element)}')
            
            print()
        print()

def main():
    content_per_page = extract_all(PDF_PATH)
    write_to_word(content_per_page, WORD_PATH)
    # get_tree(content_per_page)
    # print(content_per_page[0][7])

