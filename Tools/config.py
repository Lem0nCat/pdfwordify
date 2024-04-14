# Язык для GOOGLE TESSERACT OCR
LANG = "rus+eng"

# Путь к языковым данным для GOOGLE TESSERACT OCR
TESSDATA_PATH = ''

# Пути для временных файлов
IMAGES_PATH = "Resources/Images"
TEMP_PDF_IMAGE = f"{IMAGES_PATH}/cropped_image.pdf"
TEMP_IMAGE = f"{IMAGES_PATH}/PDF_image.png"

# Название файла
FILE_NAME = "test"

# Пути для PDF и Word файла
PDF_PATH = f"Resources/PDF_files/{FILE_NAME}.pdf"

WORD_FILES_PATH = "Resources/word_files"
WORD_PATH = f"{WORD_FILES_PATH}/{FILE_NAME}.docx"

# Настройки распознавания таблиц для pdfplumber
TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 5,  # Увеличиваем допуск для лучшего совмещения линий
    "join_tolerance": 3,
    "intersection_tolerance": 3
}
