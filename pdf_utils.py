import re

from pypdf import PdfReader


def extract_text_from_pdf(file):
    text = ''
    reader = PdfReader(file)

    num_pages = reader.get_num_pages()
    for page_number in range(num_pages):
        page = reader.get_page(page_number)
        if '/Font' in page['/Resources']:
            text += page.extract_text()
    return text

