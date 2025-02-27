# -*- coding: utf-8 -*-
import os.path
from os import makedirs

from loguru import logger
from weasyprint import HTML

from spider_to_pdf.app_config import project_root, resource_path, home_page_path, html_path, out_put_path


def init_file_name(file_name: str) -> str:
    if not file_name.endswith(".html"):
        file_name = file_name + ".html"
    return file_name


def merge_pdf(home_page_file_name: str, content_file_names: list[str], style_name: str, pdf_name: str) -> str:
    logger.info(f"merge pdf {home_page_file_name},style_name:{style_name},content_file_path:{content_file_names}")
    home_page_base_url = str(os.path.join(project_root, resource_path, style_name, home_page_path))
    pages = []
    home_page_file = os.path.join(home_page_base_url, init_file_name(home_page_file_name))
    home_page = HTML(filename=home_page_file, base_url=home_page_base_url)
    pages.extend(home_page.render().pages)
    html_page_base_url = str(os.path.join(project_root, resource_path, style_name, html_path))
    for content_file_name in content_file_names:
        content_file_path = str(os.path.join(project_root, resource_path, init_file_name(content_file_name)))
        page = HTML(filename=content_file_path, base_url=html_page_base_url)
        pages.extend(page.render().pages)

    pdf_file_path = os.path.join(project_root, out_put_path, style_name)
    if not os.path.exists(pdf_file_path):
        makedirs(pdf_file_path)
    pdf_local = os.path.join(str(pdf_file_path), pdf_name) + ".pdf"
    HTML(string="").render().copy(pages).write_pdf(pdf_local)
    return str(pdf_local)
