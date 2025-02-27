# -*- coding: utf-8 -*-

import fitz  # pymupdf

from spider_to_pdf.save_page import StyleInfo


def add_page_numbers_with_outline(input_pdf_path, out_pdf_path, style: StyleInfo):
    doc = fitz.open(input_pdf_path)
    number_color = tuple(int(color_number) for color_number in style.number_color.split(","))
    for i in range(1, len(doc)):  # jump first page
        page = doc[i]
        page.insert_text(
            (page.rect.width - 100, page.rect.height - 35),
            f"Page {i + 1}",
            fontsize=12,
            color=number_color
        )

    doc.save(out_pdf_path)
