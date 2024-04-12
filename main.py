from docx import Document

from pdf_extract import extract_all
from save_word import write_to_word_v2


# export TESSDATA_PREFIX=/usr/share/tesseract/5/tessdata

FILE_NAME = "Privacy policy"
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

def test_font_parse(pages):
    for page in pages:
        for element in page['line_format']:
            if isinstance(element, list):
                for font in element:
                    fontname, bold, italic = parse_font_info(font[0])
                    print(f"Before: {font[0]}\nAfter: {fontname}\nBold: {bold}, Italic: {italic}, Size: {font[1]}\n")


content_per_page = extract_all(PDF_PATH)
write_to_word_v2(content_per_page, WORD_PATH)
# get_tree(content_per_page, "text_from_images")

# table = extract_table(PDF_PATH, 4, 0)
# for row in table:
#     print(row)
