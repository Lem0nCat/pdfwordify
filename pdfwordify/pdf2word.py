import argparse
import os
import sys

from pdfwordify.converter import convert_to_docx


def main_cli():
    parser = argparse.ArgumentParser(
        description="Process a PDF file and save the results to a docx document in a specified directory.",
        epilog="Example usage: ./run.py --method none --lang rus+eng example.pdf /path/to/output/dir"
    )
    # Adding arguments to the command line
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file (default: configured in Tools/config.py)')
    parser.add_argument('output_dir', nargs='?', type=str, help='Directory to save the docx file (default: PDF file directory)')
    parser.add_argument('-m', '--method', type=str, choices=['stream', 'lattice', 'none'],
                        default='lattice', help='The method to extract tables from the PDF: stream, lattice, or none (default: lattice)')
    parser.add_argument('-l', '--lang', type=str, default='eng', 
                        help='A language for extracting text from images in a document (default: eng). It is possible to combine languages (For example: "rus+eng")')
    
    args = parser.parse_args()  # Parsing command line arguments
  
    try:
        print(f"Selected file: '{args.pdf_path}'. Processing...")
        # If 'none' is entered
        method = None if args.method.lower() == 'none' else args.method
        # Document conversion
        word_path = convert_to_docx(args.pdf_path, args.output_dir, method, args.lang)
        # Saving the results to a docx file
        print(f"The document has been successfully saved: '{word_path}'")
        
    except Exception as e:
        print(f"Error: {str(e)}")   # Error output if something went wrong
        sys.exit(1)     # Program termination with error code

if __name__ == "__main__":
    main_cli()
