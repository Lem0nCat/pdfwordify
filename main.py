from docx import Document

from pdf_extract import extract_all
from save_word import write_to_word_v2


# export TESSDATA_PREFIX=/usr/share/tesseract/5/tessdata

FILE_NAME = "Privacy policy"
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

content_per_page = extract_all(PDF_PATH)
write_to_word_v2(content_per_page, WORD_PATH)
# get_tree(content_per_page)
# print(content_per_page[0][7])

