from src.pdf_extract import extract_all
from src.save_word import write_to_word

import argparse
import os
import sys

from Tools.config import PDF_PATH, WORD_PATH

def get_tree(pages):
    for i, page in enumerate(pages):
        print(f'Page #{i}')
        for j, element in enumerate(page['page_content']):
            print(f'\tElement #{j}')
            
            print(f'\t\t{type(element)}')
            
            print()
        print()

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Файла '{file_path}' не существует")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Process a PDF file and save the results to a Word document in a specified directory.",
        epilog="Example usage: ./run.py example.pdf /path/to/output/dir"
    )
    parser.add_argument('pdf_path', nargs='?', type=str, default=PDF_PATH, help='The path to the PDF file (optional, default path in "Tools/config.py")')
    parser.add_argument('output_dir', nargs='?', type=str, help='The directory where the Word file will be saved (optional, if not specified, saves to the directory of the first argument)')
    parser.add_argument('--method', type=str, choices=['stream', 'lattice', 'none'],
                        default='lattice', help='The method to extract tables from the PDF: stream, lattice, or none (default: lattice)')
    
    args = parser.parse_args()

    pdf_path = args.pdf_path
    output_dir = args.output_dir
    
    if args.output_dir:
        # Создаем путь для будушего word файла
        word_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + '.docx'
        word_path = os.path.join(output_dir, word_file_name)
    elif args.pdf_path != PDF_PATH:
        # Если путь к PDF указан, но путь к Word не указан, создаём путь заменой расширения
        word_path = os.path.splitext(pdf_path)[0] + '.docx'
    else:
        # Если ничего не указано, используем значение по умолчанию для Word файла
        word_path = WORD_PATH

    check_file_exists(pdf_path)

    print(f"Selected file: '{pdf_path}'\nProcessing file...")
    
    method = None if args.method == 'none' else args.method
    
    # Обработка PDF в зависимости от выбранного метода извлечения таблиц
    content_per_page = extract_all(pdf_path, method)
    write_to_word(content_per_page, word_path)
    
    # get_tree(content_per_page)

if __name__ == "__main__":
    main()
