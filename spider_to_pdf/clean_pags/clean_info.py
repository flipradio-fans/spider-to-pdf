# -*- coding: utf-8 -*-
import urllib.parse

from bs4 import BeautifulSoup
from loguru import logger

from spider_to_pdf.app_config import config

_clean_config = config.get("clean")


def get_main_html_info(html_soup: BeautifulSoup) -> BeautifulSoup | None:
    """
    :param html_soup:
    :return:
    """
    if html_soup is None:
        logger.info("clean html info beautiful soup is None")
        return None
    return html_soup.select_one(_clean_config.get("main_info", "body"))


def clean_html_info(html_soup: BeautifulSoup) -> BeautifulSoup | None:
    """
    clean html info
    :param html_soup: main html soup
    :return: cleaned html soup
    """
    logger.info("begin clean html info.")
    if html_soup is None:
        logger.info("clean html info beautiful soup is None")
        return None
    filter_elements(html_soup)
    filter_id_elements(html_soup)
    filter_mark_info(html_soup)
    cut_off_page(html_soup)
    return html_soup


def filter_elements(html_soup: BeautifulSoup):
    """
    filter elements
    :param html_soup:
    :return:
    """
    logger.info("running filter elements")
    need_filter_elements = _clean_config.get("need_filter_elements", [])
    logger.info(f"clean config need_filter_elements:{need_filter_elements}")
    if need_filter_elements:
        logger.info("There are some element need filter")
        for need_filter_element in need_filter_elements:
            logger.debug(f"filter element find path:{need_filter_element}")
            filter_element = html_soup.select_one(need_filter_element)
            logger.debug(f"filter element :{filter_element}")
            if filter_element:
                logger.debug(f"find path:{need_filter_element} is decompose.")
                filter_element.decompose()


def filter_id_elements(html_soup: BeautifulSoup):
    """
    filter id elements
    :param html_soup:
    :return:
    """
    logger.info("running filter id elements")
    need_filter_ids = _clean_config.get("need_filter_ids", [])
    logger.info(f"clean config need_filter_ids:{need_filter_ids}")
    if need_filter_ids:
        logger.info("There are some id element need filter")
        for need_filter_id in need_filter_ids:
            logger.debug(f"filter element id:{need_filter_id}")
            filter_element = html_soup.find(id=f"{urllib.parse.quote(need_filter_id)}")
            logger.debug(f"filter element :{filter_element}")
            if filter_element:
                logger.debug(f"find path:{filter_element} is decompose.")
                filter_element.decompose()


def filter_mark_info(html_soup: BeautifulSoup):
    logger.info("running filter mark info")
    need_filter_mark_infos = _clean_config.get("need_filter_mark_info", {})
    logger.info(f"clean config filter_mark_info:{need_filter_mark_infos}")
    if need_filter_mark_infos:
        logger.info("There are some mark info need filter")
        for need_filter_mark_info in need_filter_mark_infos:
            for element_name, element_text in need_filter_mark_info.items():
                logger.debug(f"clean mark info element_name:{element_name},element_text:{element_text} ")
                all_elements = html_soup.find_all(element_name)
                logger.debug(f"find elements :{all_elements}")
                if all_elements:
                    for p in all_elements:
                        if p and p.text and p.text.strip() in element_text:
                            logger.debug(f"clean p:{p}")
                            p.decompose()


def cut_off_page(html_soup: BeautifulSoup):
    logger.info("running cut off page")
    need_cut_off_elements = _clean_config.get("need_cut_off_mark", [])
    logger.info(f"clean config need_cut_off_elements:{need_cut_off_elements}")
    if need_cut_off_elements:
        logger.info("There are some element need cut off.")
        for element in need_cut_off_elements:
            all_elements = html_soup.find_all(element)
            if all_elements:
                last_element = all_elements[-1]
                if last_element:
                    print(f"need cut off element:{last_element}")
                    content_after_last = last_element.find_next_siblings()
                    if content_after_last:
                        for cut_off_element in content_after_last:
                            cut_off_element.decompose()
                    last_element.decompose()
