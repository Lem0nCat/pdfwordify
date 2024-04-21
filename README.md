# PDF Extractor

PDF Extractor — это инструмент для извлечения текста и таблиц из PDF-файлов и сохранения этих данных в формате Microsoft Word. Этот проект предназначен для автоматизации процесса переноса информации из PDF в более удобные для редактирования и обработки форматы.

## Особенности

- Извлечение текста из PDF.
- Извлечение текста из сканированных страниц в PDF.
- Извлечение таблиц из PDF.
- Сохранение извлеченной информации в файл Word.

## Требования к системе

Проект разработан на Python и требует следующего:
- Python 3.12 или выше. (Скорее всего будут работать и другие, не проверял)
- Библиотеки Python, указанные в файле `requirements.txt`.
- [Google tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Установка

Перед началом работы убедитесь, что у вас установлен Python и pip. Затем выполните следующие шаги:

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/Lem0nCat/PDF_extractor.git
   ```
2. Перейти в директорию с установленным репозиторием.
3. Установить [Google tesseract OCR](https://github.com/tesseract-ocr/tesseract):
4. Установить зависимости из файла:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

### Важно

Если ваши языковые данные для Tesseract OCR не находятся в папке по умолчанию, то укажите верный путь в файле `Tools/config.py` в переменной `TESSDATA_PATH`. По умолчанию строка пустая, то есть **путь указан по умолчанию**.

### Простое использование

Запустите исполняемый файл с необходимыми аргументами

```bash
run.py [-h] [--method {stream,lattice,none}] [pdf_path] [output_dir]
```

#### Аргументы

- `--method`:
   - **Описание**: Метод извлечения таблиц из файла.
   - **Обязательный**: Нет
   - **По умолчанию**: Используется метод `lattice`
   - **Виды**:

      - `--method lattice` для таблиц, которые имеют четкие границы. 

         <img src="Resources/Images/GitHub Images/image.png" alt="Таблица с четкими границами" width="500"/>

      - `--method stream` для таблиц, которые имеют четких границ. 

         <img src="Resources/Images/GitHub Images/image2.png" alt="Таблица без границ" width="500"/>

      - `--method none` если в документе нет таблиц.
   - **Пример**: `./run.py --method stream dir/example.pdf`

- `example.pdf`: 
  - **Описание**: Путь к входному файлу PDF, который нужно преобразовать.
  - **Обязательный**: Нет
  - **По умолчанию**: Используется файл из `Tools/config.py`
  - **Пример**: `./run.py example.pdf`

- `/path/to/output/dir`:
  - **Описание**: Путь к папке, в которую будет сохранен docx файл.
  - **Обязательный**: Нет
  - **По умолчанию**: Используется директория файла PDF
  - **Пример**: `./run.py example.pdf ~/Desktop`


Если не будет указан ни один аргумент, пути к PDF и Word файлу будут взяты из `Tools/config.py`

### Альтернативное использование

1. Переместите нужный PDF файл в папку `Resources/PDF_files`.
2. Укажите название PDF файла в файле `Tools/config.py` в переменной `FILE_NAME`.
3. Для запуска программы выполните:
   ```bash
   ./run.py
   ```

## Конфигурация

Для настройки параметров извлечения данных отредактируйте файл `Tools/config.py`.

## Разработка

Проект включает следующие основные компоненты:

- **main.py**: Точка входа в программу.
- **pdf_extract.py**: Модуль для обработки и извлечения данных из PDF.
- **Папка Classes**: Содержит определения классов для элементов PDF.
- **Папка Tools**: Вспомогательные инструменты для извлечения текста, изображений и таблиц.
- **Папка Resources**: Служит папкой для PDF и Word файлов, и изображений
