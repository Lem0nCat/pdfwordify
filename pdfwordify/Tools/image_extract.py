from PIL import Image   # To open an image

import fitz # PyMuPDF to extract images from PDFs

import pytesseract  # To perform OCR to extract text from images

import os       # To delete additionally created files
import tempfile # To create temporary files


def extract_images(document, page_index):
    """
    Extracts all images from a specified page of the document and saves them to temporary files.
    
    Args:
        document (fitz.Document): The document from which images are being extracted.
        page_index (int): The index of the page in the document from which images are extracted.
    
    Returns:
        list of tempfile.TemporaryFile: A list of temporary file objects, each containing an image from the page.
    """
    page = document.load_page(page_index)   # Load the page
    # Extract images from the page
    image_list = page.get_images(full=True)
    temp_images = []    # Temporary storage for extracted images
    
    # Save each image from the page
    for img in image_list:
        xref = img[0]   # Image XREF
        base_image = document.extract_image(xref)
        image_bytes = base_image['image']   # Extract image data
        
        # Create a temporary file for the image
        temp_image = tempfile.NamedTemporaryFile(delete=False)
        
        # Write image data to the file
        with open(temp_image.name, "wb") as img_file:
            img_file.write(image_bytes)
        temp_images.append(temp_image)
        
    return temp_images


def image_to_text(temp_image, lang):
    """
    Converts an image file into text using Optical Character Recognition (OCR).
    
    Args:
        temp_image (file object): The image file object to be converted.
        lang (str): The language of the text to be extracted.
    
    Returns:
        str: The text extracted from the image.
    """
    img = Image.open(temp_image.name)  # Open the image file
    text = pytesseract.image_to_string(img, lang=lang)  # Extract text from the image using OCR
    return text

def finalize_temp_images(temp_images):
    """
    Closes and deletes all temporary image files.
    
    Args:
        temp_images (list of file objects): List of temporary image file objects.
    """
    for temp_image in temp_images:  # Iterate through each image
        temp_image.close()  # Close the file
        os.remove(temp_image.name)  # Remove the file from the filesystem

class ConversionBackend:
    """Class for handling the conversion of PDF pages to PNG format."""
    def convert(self, pdf_path, png_path):
        """
        Converts all pages of a PDF file to PNG images.

        Args:
            pdf_path (str): The path to the PDF file to convert.
            png_path (str): The base path to save the PNG images.
        """
        doc = fitz.open(pdf_path)  # Open the PDF document
        for page in doc.pages():  # Process each page
            pix = page.get_pixmap()  # Convert page to a pixmap (image)
            pix.save(png_path)  # Save the pixmap as a PNG file
