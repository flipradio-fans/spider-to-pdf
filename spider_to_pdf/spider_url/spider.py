# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup
from loguru import logger

from spider_to_pdf.app_config import config

_spider_config = config.get("spider")

_config_filter_urls = [
    filter_url if filter_url.startswith("http") else "".join([_spider_config.get("base_url"), "/", filter_url, "/"])
    for filter_url in
    _spider_config.get("need_filter_url", [])]


class CrawlInfo:
    """
    :param url: crawl url
    :param soup_info: crawl url beautiful soup object
    """

    def __init__(self, url: str, lastmod_timestamp: int, soup_info: BeautifulSoup):
        self.url = url
        self.lastmod_timestamp = lastmod_timestamp
        self.soup_info = soup_info


def transform_time_str_to_timestamp(time_str: str) -> int:
    """
    transform ghost blog time str to timestamp
    :param time_str: time str
    :return: timestamp
    """
    datetime_object = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    # 转换为时间戳
    return int(datetime_object.timestamp())


def download_ghost_blog_website_xml(website_url: str, filter_url: list[str] = None):
    """
    :param website_url: ghost blog website`s xml url.
    :param filter_url: filter url incremental update download
    :return: website all CrawlInfos
    """
    logger.info(f"download_ghost_blog_website_xml function download ghost blog website xml ,website_url:{website_url}")
    if filter_url is None:
        filter_url = _config_filter_urls
    else:
        filter_url.extend(_config_filter_urls)
    web_sit_xml_info = request_url(website_url)
    base_soup = BeautifulSoup(web_sit_xml_info, "html.parser")
    sitemap_table_rows = base_soup.find_all('url')
    logger.debug(f"download ghost blog website sitemap_table_rows:{sitemap_table_rows}")
    if sitemap_table_rows:
        logger.info(f"on the website has {len(sitemap_table_rows)} rows url need crawl")
        for row in sitemap_table_rows:
            loc = row.find_next("loc")
            lastmod = row.find_next("lastmod")
            last_timestamp = None
            if lastmod is not None:
                last_timestamp = transform_time_str_to_timestamp(lastmod.text)
            if loc and loc.text not in filter_url:
                yield CrawlInfo(loc.text, last_timestamp, BeautifulSoup(request_url(loc.text), "html.parser"))


def crawl_url(begin_url: str, base_url: str, deep: int = 0, result_url: set[str] = None):
    """
    :param begin_url: begin crawl url
    :param base_url: filter not base_url's a href
    :param deep: recursion deep ,Prevent crawling too far.
    :param result_url: already crawl url ,Prevent repeat crawl
    :return: class CrawlInfo

    Start crawling from the beginning web url, crawling the URL and content of the website at a specified depth
    """
    if result_url is None:
        result_url = ()
    logger.debug(f"begin_url is {begin_url} and deep = {deep}")
    if deep == _spider_config.get("crawl_deep", 3):
        return

    base_soup = BeautifulSoup(request_url(begin_url), "html.parser")
    if base_soup:
        a_tags = base_soup.find_all("a")
        if a_tags:
            for a_tag in a_tags:
                if "href" in a_tag.attrs:
                    a_url = a_tag["href"]
                    if a_url.startswith(base_url) and a_url not in result_url:
                        result_url.add(a_tag["href"])
                        yield CrawlInfo(a_tag["href"], 0, base_soup)
                        yield from crawl_url(a_url, base_url, deep + 1, result_url)


def request_url(url: str, retry: int = 0) -> str:
    """
    :param url:
    :param retry:
    :return:
    This is a download page tool, Download the webpage using requests.
    """
    if retry == _spider_config.get("download_retry_number", 0):
        return ""
    try:
        responses = requests.get(url)
        sleep(1)
        if responses.status_code != 200:
            logger.error(f"request field url: {url} status_code: {responses.status_code}")
        return responses.text
    except Exception as e:
        logger.error(f"request field url: {url},e:{e.args} ")
        return request_url(url, retry + 1)
