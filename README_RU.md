# pdfwordify

**pdfwordify** — это инструмент для извлечения текста и таблиц из PDF-файлов и сохранения этих данных в формате docx(Word). Этот проект предназначен для автоматизации процесса переноса информации из PDF в более удобные для редактирования и обработки форматы.

## Особенности

- Извлечение текста из PDF.
- Извлечение текста из сканированных страниц в PDF.
- Извлечение таблиц из PDF.
- Сохранение извлеченной информации в файл Word.


## Как использовать

- Установите Python 3.10 или новее.

- Установите [Google tesseract OCR](https://github.com/tesseract-ocr/tesseract)

- Установите [Ghostscript](https://www.ghostscript.com/)

- Установите библиотеку с помощью pip:
   ```bash
   pip install pdfwordify
   ```

- Используйте интерфейс командной строки для конвертации из PDF в docx.
   ```bash
   pdfwordify example.pdf
   ```

- Или используйте его с Python.
   ```python
   from pdfwordify.converter import convert_to_docx

   convert_to_docx("example.pdf")
   ```

### Аргументы

В данном разделе будут приведены аргументы использования конвертера. Они подходят как для использования внутри командной строки, так и для использования внутри Python.

- `pdf_path`: 
  - **Описание**: Путь к входному файлу PDF, который нужно преобразовать.
  - **Обязательный**: Да
   - **Пример**: 
      - В терминале: `pdfwordify dir/example.pdf`
      - В коде: `convert_to_docx("dir/example.pdf")`

- `output_dir`:
  - **Описание**: Путь для docx файла. Может быть как путь к папке, так и путь с названием или полный путь с указанием расширением файла(docx).
  - **Обязательный**: Нет
  - **По умолчанию**: Используется директория файла PDF
   - **Пример**: 
      - В терминале: `pdfwordify dir/example.pdf /output/path/`
      - В коде: `convert_to_docx("dir/example.pdf", "/output/path/")`

- `method`:
   - **Описание**: Метод извлечения таблиц из файла.
   - **Обязательный**: Нет
   - **По умолчанию**: Используется метод `lattice`
   - **Виды**:
      - `lattice` для таблиц, которые имеют четкие границы. 

         <img src="docs/images/lattice_example_table.png" alt="Таблица с четкими границами" width="500"/>

      - `stream` для таблиц, которые имеют четких границ. 

         <img src="docs/images/stream_example_table.png" alt="Таблица без границ" width="500"/>

      - `None` если в документе нет таблиц.
   - **Пример**: 
      - В терминале: `pdfwordify --method stream dir/example.pdf`
      - В коде: `convert_to_docx("example.pdf", method=None)`

- `lang`:
   - **Описание**: Язык для извлечения текста из изображений внутри документа с помощью Google Tesseract OCR.
   - **Обязательный**: Нет
   - **По умолчанию**: Используется язык `eng`
   - **Примечание**: Возможно совмещение языков. Например: `rus+eng`
   - **Пример**: 
      - В терминале: `pdfwordify --lang rus+eng dir/example.pdf`
      - В коде: `convert_to_docx("example.pdf", lang="rus+eng")`

## Настройки

Для дополнительной настройки параметров отредактируйте файл `config.py`.
