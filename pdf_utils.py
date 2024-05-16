import json
import re

import fitz

import pandas as pd
import numpy as np


def remove_non_ascii(text):
    return ''.join(char for char in text if ord(char) < 128)


def extract_blocks(pdf_document) -> dict:
    # Iterate through each page of the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        block_dict = {}
        page_num = 1
        for page in pdf_document:  # Iterate all pages in the document
            file_dict = page.get_text('dict')  # Get the page dictionary
            blocks = file_dict['blocks']  # Get the block information
            block_dict[page_num] = blocks  # Store in block dictionary
            page_num += 1  # Increase the page value by 1

    return block_dict


def extract_spans(block_dict: dict):
    rows = []
    for page_num, blocks in block_dict.items():
        for block in blocks:
            if block['type'] != 0:
                continue

            for line in block['lines']:
                for span in line['spans']:
                    text = remove_non_ascii(span['text'])
                    if text.replace(" ", "") == "":
                        continue

                    xmin, ymin, xmax, ymax = list(span['bbox'])
                    font_size = span['size']
                    span_font = span['font']
                    is_upper = False
                    is_bold = False
                    if "bold" in span_font.lower():
                        is_bold = True
                    if re.sub("[\(\[].*?[\)\]]", "", text).isupper():
                        is_upper = True

                    rows.append((xmin, ymin, xmax, ymax, text, is_upper, is_bold, span_font, font_size))

    span_df = pd.DataFrame(rows, columns=['xmin', 'ymin', 'xmax', 'ymax', 'text', 'is_upper', 'is_bold', 'span_font',
                                          'font_size'])
    return span_df


def extract_unique_styles(span_df) -> dict:
    span_scores = []
    special = '[(_:/,#%\=@)]'

    for index, span_row in span_df.iterrows():
        score = round(span_row.font_size)
        text = span_row.text
        if not re.search(special, text):
            if span_row.is_bold:
                score += 1
            if span_row.is_upper:
                score += 1
        span_scores.append(score)

    values, counts = np.unique(span_scores, return_counts=True)

    style_dict = {}
    for value, count in zip(values, counts):
        style_dict[value] = count
    sorted(style_dict.items(), key=lambda x: x[1])

    p_size = max(style_dict, key=style_dict.get)
    idx = 0
    tag = {}
    for size in sorted(values, reverse=True):
        idx += 1
        if size == p_size:
            idx = 0
            tag[size] = 'p'
        if size > p_size:
            tag[size] = 'h{0}'.format(idx)
        if size < p_size:
            tag[size] = 's{0}'.format(idx)

    span_tags = [tag[score] for score in span_scores]
    span_df['tag'] = span_tags


def extract_text_from_pdf(pdf_bytes):
    # Open the PDF bytes with PyMuPDF
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    block_map = extract_blocks(pdf_document)
    span_dataframe = extract_spans(block_map)
    style_map = extract_unique_styles(span_dataframe)
    pdf_document.close()
    print(json.dumps(span_dataframe.to_dict('records'), indent=2))
    return ""
