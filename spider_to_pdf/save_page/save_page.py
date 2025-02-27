# -*- coding: utf-8 -*-
import copy
import os.path

from bs4 import BeautifulSoup
from loguru import logger

from spider_to_pdf.app_config import config, project_root, resource_path, html_path

_save_config = config.get("save")
_resource_path = os.path.join(project_root, resource_path)
_save_html_path = os.path.join(str(_resource_path), html_path)
_home_page_content_element = _save_config.get("home_page_content_element")


class StyleInfo:
    def __init__(self, home_page_path: str, base_template_path: str, home_page_style_path: list[str],
                 page_style_path: list[str], number_color: str, style_name: str):
        self.home_page = home_page_path
        self.base_template_path = base_template_path
        self.home_page_style_path = home_page_style_path
        self.page_style_path = page_style_path
        self.number_color = number_color
        self.style_name = style_name
        try:
            with open(os.path.join(str(_resource_path), style_name, home_page_path), "r",
                      encoding="UTF-8") as home_page_info:
                self.home_page_path_soup = BeautifulSoup(home_page_info.read(), "html.parser")
        except FileNotFoundError as error:
            logger.error(f"{style_name} style don't has home page error:{error.args}")

        try:
            with open(os.path.join(str(_resource_path), style_name, base_template_path), "r",
                      encoding="UTF-8") as base_template_path:
                self.base_template_path_soup = BeautifulSoup(base_template_path.read(), "html.parser")
        except FileNotFoundError as error:
            logger.error(f"{style_name} style don't has base template path error:{error.args}")


_select_module = _save_config.get("select_module", [])
_page_module_config = _save_config.get("page_module", {})

style_list = [StyleInfo(style_info.get("home_page_path", ""),
                        style_info.get("base_template_path", ""),
                        style_info.get("home_page_style_path", []),
                        style_info.get("page_style_path", []),
                        style_info.get("number_color", ""),
                        style_info.get("style_name", "")) for style_info in
              _page_module_config if style_info.get("style_name", "") in _select_module]


def composite_template(html_soup: BeautifulSoup, style_info: StyleInfo) -> BeautifulSoup:
    if style_info.base_template_path_soup is None:
        logger.error("composite template error base template soup is None")
        return html_soup
    template_soup = copy.deepcopy(style_info.base_template_path_soup)
    body_tag = template_soup.find("body")
    body_tag.append(html_soup)
    return template_soup


def add_style(html_soup: BeautifulSoup, style_info: StyleInfo, path_name: str = "page_style_path"):
    if not getattr(style_info, path_name):
        logger.info("There aren't style in this styles")
        return html_soup
    for stype_css_file in getattr(style_info, path_name):
        new_css_link = html_soup.new_tag('link', rel='stylesheet', type='text/css',
                                         href=f'{os.path.join("..", stype_css_file)}')
        html_soup.find("head").append(new_css_link)
    return html_soup


def init_title(html_soup: BeautifulSoup) -> BeautifulSoup:
    logger.info("init title")
    title_source = html_soup.select_one(_save_config.get("title_source", "body > main > article > header > h1"))
    if not title_source:
        logger.error("title source is not exists")
    title_target = html_soup.select_one(_save_config.get("title_target", "head > title"))
    if not title_target:
        logger.error("title target is not exists")
    title_target.string = title_source.string
    return html_soup


def init_file_name(file_name: str) -> str:
    if not file_name.endswith(".html"):
        file_name = file_name + ".html"
    return file_name


def init_home_page_content_element(style_info: StyleInfo, content: str) -> BeautifulSoup | None:
    if style_info.home_page_path_soup is None:
        logger.error("init home page content home page path soup is None")
        return None
    home_page_info = copy.deepcopy(style_info.home_page_path_soup)
    content_element = home_page_info.find_next(_home_page_content_element)
    content_element.string = content
    return home_page_info


def save_page(html_soup: BeautifulSoup, style_name: str, file_name: str, dir_path: str = html_path) -> str | None:
    """
    save html page to local and return local path
    :param dir_path: default save dir
    :param style_name: html_soup style name
    :param file_name: save html file name
    :param html_soup: html info soup
    :return: local path
    """
    if file_name is None:
        logger.error("file name is must be not None")
        return None
    file_name = init_file_name(file_name)
    file_path = os.path.join(style_name, dir_path)
    result_file_path = os.path.join(file_path, file_name)
    local_file_path = os.path.join(project_root, result_file_path)
    if os.path.exists(local_file_path):
        logger.info(f"save page file path is exists result_file_path:{result_file_path}")
        return result_file_path
    local_path = os.path.join(project_root, resource_path, style_name, dir_path)
    if not os.path.isdir(local_path):
        logger.error(f"save page file path is not exists file_path:{local_path}")
        try:
            os.makedirs(local_path)
            logger.info("save page file path created success")
        except Exception as e:
            logger.error(f"save page file path created failed e:{e.args}")
    with open(os.path.join(str(local_path), file_name), "w+", encoding="UTF-8") as page_file:
        page_file.write(html_soup.prettify())
    return result_file_path


def clean_page(style_name: str, file_name: str) -> bool:
    """
    clean html page
    :param style_name: style name
    :param file_name: htmp name
    :return:
    """
    if file_name is None:
        logger.error("file name is must be not None")
        return False
    file_name = init_file_name(file_name)
    clean_page_path = os.path.join(str(_resource_path), style_name, html_path, file_name)
    if not os.path.exists(clean_page_path):
        logger.error(f"clean page is not exists clean_page_path:{clean_page_path}")
        return True
    with open(clean_page_path, "w", encoding="UTF-8") as f:
        pass
    return True
