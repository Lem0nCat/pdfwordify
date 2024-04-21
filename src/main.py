import argparse
import os
import sys

from src.pdf_extract import extract_all  # Импорт функции для извлечения данных из PDF
from src.save_word import write_to_word  # Импорт функции для записи данных в файл Word

from Tools.config import PDF_PATH, WORD_PATH  # Импорт путей по умолчанию из конфигурационного файла


def check_file_exists(file_path):
    """Проверяет наличие файла по указанному пути."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist!")

def main():
    parser = argparse.ArgumentParser(
        description="Process a PDF file and save the results to a Word document in a specified directory.",
        epilog="Example usage: ./run.py example.pdf /path/to/output/dir"
    )
    # Добавление аргументов для командной строки
    parser.add_argument('pdf_path', nargs='?', type=str, default=PDF_PATH, help='Path to the PDF file (default: configured in Tools/config.py)')
    parser.add_argument('output_dir', nargs='?', type=str, help='Directory to save the Word file (default: PDF file directory)')
    parser.add_argument('--method', type=str, choices=['stream', 'lattice', 'none'],
                        default='lattice', help='The method to extract tables from the PDF: stream, lattice, or none (default: lattice)')
    
    args = parser.parse_args()  # Парсинг аргументов командной строки

    pdf_path = args.pdf_path
    

    if args.output_dir:
        # Формирование имени файла Word из имени PDF
        word_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + '.docx'
        # Построение полного пути к файлу Word
        word_path = os.path.join(args.output_dir, word_file_name)
    elif pdf_path == PDF_PATH:  # Если не указан ни один аргумент
        word_path = WORD_PATH
    else:   # Если путь к PDF указан, но путь к Word не указан, создаём путь заменой расширения
        word_path = os.path.splitext(pdf_path)[0] + '.docx'
    
    try:
        check_file_exists(pdf_path) # Проверка наличия PDF файла
        print(f"Selected file: '{pdf_path}'. Processing...")
    
        # Обработка PDF в зависимости от выбранного метода извлечения таблиц
        method = None if args.method == 'none' else args.method
        content_per_page = extract_all(pdf_path, method)
        
        # Сохранение результатов в файл Word
        print('Saving file...')
        write_to_word(content_per_page, word_path)
    except Exception as e:
        print(f"Error: {str(e)}")   # Вывод ошибки, если что-то пошло не так
        sys.exit(1)     # Завершение программы с кодом ошибки

if __name__ == "__main__":
    main()
