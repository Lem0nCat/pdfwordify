# Язык для GOOGLE TESSERACT OCR
LANG = "rus+eng"

# Путь к языковым данным для GOOGLE TESSERACT OCR
TESSDATA_PATH = '/usr/share/tesseract/5/tessdata'

# Пути для временных файлов
TEMP_PDF_IMAGE = "Resources/Images/cropped_image.pdf"
TEMP_IMAGE = "Resources/Images/PDF_image.png"

# Настройки распознавания таблиц для pdfplumber
TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines_strict",
    "snap_tolerance": 5,  # Увеличиваем допуск для лучшего совмещения линий
    "join_tolerance": 3,
    "intersection_tolerance": 3,
    "min_words_horizontal": 2  # Ищем минимум 2 слова для разделения строк по тексту
}