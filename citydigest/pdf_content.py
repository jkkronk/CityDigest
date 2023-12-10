import PyPDF2
import os

def pdf_to_string(pdf_path: str) -> str:
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = os.path.basename(pdf_path)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += f"\n \n NEW PAGE: \n {page.extract_text()}"
    return text

def get_all_pdfs_in_directory(directory: str) -> list[str]:
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]



