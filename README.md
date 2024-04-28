# pdfwordify

**pdfwordify** is a tool for extracting text and tables from PDF files and saving this data in docx(Word) format. This project is designed to automate the process of transferring information from PDF to formats that are easier to edit and process.

## Features

- Text extraction from PDF.
- Extract text from scanned pages to PDF.
- Extract tables from PDF.
- Save extracted information to a Word file.


## How to use

- Install Python 3.10 or newer.

- Install [Google tesseract OCR](https://github.com/tesseract-ocr/tesseract)

- Install the library using pip:
   ```bash
   pip install pdfwordify
   ```

- Use the command-line interface to convert from PDF to docx.
   ```bash
   pdfwordify example.pdf
   ```

- Or use it with Python.
   ```python
   from pdfwordify.converter import convert_to_docx

   convert_to_docx("example.pdf")
   ```

### Arguments

This section will provide arguments for using the converter. They are suitable for use within the command line as well as for use within Python.

- `pdf_path`: 
  - **Description**: The path to the input PDF file to be converted.
  - **Required**: Yes
   - **Example**: 
      - In terminal: `pdfwordify dir/example.pdf`.
      - In code: `convert_to_docx("dir/example.pdf")`.

- `output_dir`:
  - **Description**: The path for the docx file. Can be either a folder path, a named path, or a full path specifying the file(docx) extension.
  - **Required**: No
  - **Default**: PDF file directory is used
   - **Example**: 
      - In terminal: `pdfwordify dir/example.pdf /output/path/`.
      - In code: `convert_to_docx("dir/example.pdf", "/output/path/")`

- `method`:
   - **Description**: Method for extracting tables from a file.
   - **Required**: No
   - **Default**: `lattice`
   - **Types**:
      - `lattice` for tables that have distinct boundaries. 

         <img src="docs/images/lattice_example_table.png" alt="Table with clear boundaries" width="500">

      - `stream` for tables that have clear borders. 

         <img src="docs/images/stream_example_table.png" alt="Table with no borders" width="500">

      - `None` if there are no tables in the document.
   - **Example**: 
      - In terminal: `pdfwordify --method stream dir/example.pdf`.
      - In code: `convert_to_docx("example.pdf", method=None)`.

- `lang`:
   - **Description**: Language for extracting text from images within a document using Google Tesseract OCR.
   - **Required**: No
   - **Default**: `eng`
   - **Note**: It is possible to combine languages. For example: `rus+eng`
   - **Example**: 
      - In terminal: `pdfwordify --lang rus+eng dir/example.pdf`.
      - In code: `convert_to_docx("example.pdf", lang="rus+eng")`.

## Settings

To further customize the settings, edit the `config.py` file.
