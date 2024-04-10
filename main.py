from docx import Document


from pdf_extract import extract_all
from save_word import write_to_word


# export TESSDATA_PREFIX=/usr/share/tesseract/5/tessdata

FILE_NAME = "test"
PDF_PATH = f"Resources/PDF_files/{FILE_NAME}.pdf"
WORD_PATH = f"Resources/word_files/{FILE_NAME}.docx"

def get_tree(pages, key='line_format'):
    for i, page in enumerate(pages):
        print(f'Page #{i}')
        for j, element in enumerate(page[key]):
            print(f'\tElement #{j}')
            if isinstance(element, list):
                for font in element:
                    print(f"\t\t{font}")
            else:
                print(f'\t\t{element}')
            print()
        print()

text_per_page = extract_all(PDF_PATH)
# get_tree(text_per_page)

# for page in text_per_page:
#     print(len(page['line_format']))
#     print(len(page['page_content']))






write_to_word(text_per_page, WORD_PATH)


