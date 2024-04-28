import os

from pdfwordify.pdf_extract import extract_all  # Import function to extract data from PDF
from pdfwordify.save_word import write_to_word, process_paths  # Import a function to write data to a docx file


def convert_to_docx(pdf_path, output_dir=None, method='lattice', ocr_text_lang='eng'):
    """
    Converts data from a PDF file to a docx document using the selected table extraction method.

    The function extracts text, images and tables from the file and saves the results to a docx file.

    Args:
        pdf_path (str): The path to the PDF file to be converted.
        word_path (str, optional): The path where the result will be saved in docx format.
        method (str, optional): The method to extract the tables from the PDF. Possible values:
                                    - 'lattice' (default): To process tables, with a pronounced grid line.
                                    - 'stream': For processing tables, without grid separations.
                                    - None: If there are no tables in your document.
        ocr_text_lang (str, optional): The language for OCR (Optical Character Recognition) used when processing images in PDF.
                                       processing images in PDF. The default is 'eng'.
                                       Language combinations can be used (Example: 'rus+eng').

    Return:
        str: Returns the path to the saved file

    Raises:
        RuntimeError: Returns an error if an error occurred while processing the file.

    Example:
        convert_to_word("input.pdf", "output.docx")
        convert_to_word("input.pdf", "/output/dir/", method="stream", ocr_text_lang="rus")
    """
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The file '{pdf_path}' does not exist!")
    
        # PDF processing depending on the selected table extraction method
        content_per_page = extract_all(pdf_path, method, ocr_text_lang)
        
        # Processing a custom docx path
        docx_path = process_paths(pdf_path, output_dir)
        # Saving the results to a docx file
        write_to_word(content_per_page, docx_path)
        return docx_path
    except RuntimeError as e:
        raise RuntimeError(f"Failed to convert file: {e}")   # Call an error if something goes wrong    
