from src.pdf_extract import extract_all
from src.save_word import write_to_word

from Tools.config import PDF_PATH, WORD_PATH

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

