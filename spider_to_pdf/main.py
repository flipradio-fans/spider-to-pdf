# -*- coding: utf-8 -*-
import calendar
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import Optional

from app_config import config, run_module, grouping_rules, base_url
from caches import CacheInfo, load_cache, clean_all_cache, update_cache, LocalPathInfo
from clean_pags import get_main_html_info, clean_html_info, processing_ghost_blog_html_img
from convert_to_pdf import merge_pdf, add_page_numbers_with_outline
from log_config import logger
from save_page import style_list, composite_template, add_style, init_title, save_page, init_home_page_content_element
from spider_to_pdf.app_config import home_page_path
from spider_url import download_ghost_blog_website_xml, CrawlInfo

_spider_config = config.get("spider")
website_url = _spider_config.get("website_url", "https://fearnation.club/sitemap-posts.xml")


def judge_cache_is_exists(cache: CacheInfo):
    style_names = [style.style_name for style in style_list]
    if not cache.local_path_info:
        return False
    path_style_names = [local_path_info.style_name for local_path_info in cache.local_path_info]
    for style_name in style_names:
        if style_name not in path_style_names:
            return False
    return True


def clean_page(crawl_info: CrawlInfo) -> CrawlInfo:
    page_info = get_main_html_info(crawl_info.soup_info)
    page_info = clean_html_info(page_info)
    crawl_info.soup_info = processing_ghost_blog_html_img(page_info)
    return crawl_info


def inti_sit_name(url_value: str) -> Optional[str]:
    if url_value is None:
        return None
    return url_value.replace(base_url, "")[1:][:-1]


def clean_and_convert_crawl_info_page(crawl_info: CrawlInfo) -> CacheInfo | None:
    crawl_info = clean_page(crawl_info)
    if crawl_info is None:
        return None
    return convert_crawl_info_to_page(crawl_info)


def convert_crawl_info_to_page(crawl_info: CrawlInfo) -> CacheInfo:
    sit_name = inti_sit_name(crawl_info.url)
    local_path_info = []
    for style in style_list:
        composite_info = composite_template(crawl_info.soup_info, style)
        composite_info = add_style(composite_info, style)
        composite_info = init_title(composite_info)
        local_path_info.append(LocalPathInfo(style.style_name, save_page(composite_info, style.style_name, sit_name)))
    return CacheInfo(sit_name, crawl_info.url, crawl_info.lastmod_timestamp, local_path_info)


def init_crawl_data() -> list[CacheInfo]:
    caches = load_cache()
    if not style_list:
        logger.error("style info not found")
        raise ValueError("style info not found")
    right_caches = [cache for cache in caches if judge_cache_is_exists(cache)]
    filter_urls = [cache.page_url for cache in right_caches]
    with ProcessPoolExecutor() as executor:
        new_crawl_caches_infos = list(
            executor.map(clean_and_convert_crawl_info_page,
                         download_ghost_blog_website_xml(website_url, filter_urls)))
    clean_all_cache()
    all_caches = list(right_caches)
    has_error = False
    if None in new_crawl_caches_infos:
        all_caches.extend(list(filter(lambda x: x is not None, new_crawl_caches_infos)))
        has_error = True
    else:
        all_caches.extend(new_crawl_caches_infos)
    sorted_time_list = sorted(all_caches, key=lambda x: x.page_time)
    update_cache(sorted_time_list)
    if has_error:
        raise RuntimeError("crawl data not complete,The crawled content has been cached. Please execute again.")
    return sorted_time_list


class HomePageInfo:
    def __init__(self, home_page_name: str, home_page_element_content: str, cache_infos: list[CacheInfo]):
        self.home_page_name = home_page_name
        self.home_page_element_content = home_page_element_content
        self.cache_infos = cache_infos


def get_year_month_between(start_timestamp, end_timestamp) -> list[str]:
    start_date = datetime.fromtimestamp(start_timestamp)
    end_date = datetime.fromtimestamp(end_timestamp)

    # save result data
    year_month_list = []

    current_date = start_date
    while current_date <= end_date:
        year_month_list.append(f"{current_date.year}-{current_date.month:02d}")
        # add one year
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)

    return year_month_list


def is_last_day_of_month(timestamp):
    # transform to date
    date = datetime.fromtimestamp(timestamp)

    # get current mouth last day
    _, last_day = calendar.monthrange(date.year, date.month)

    # is it the month last day
    return date.day == last_day


def init_home_page_month_info() -> list[HomePageInfo]:
    if len(all_cache_infos) < 2:
        logger.warning("cache page too small can't convert to pdf")
        return []
    first_cache = all_cache_infos[0]
    last_cache = all_cache_infos[-1]
    between_times = get_year_month_between(first_cache.page_time, last_cache.page_time)
    if not is_last_day_of_month(last_cache.page_time):
        if len(between_times) <= 1:
            return []
        between_times = between_times[:-1]
    result = []
    if between_times:
        cache_group = {}
        for cache_info in all_cache_infos:
            page_datetime = datetime.fromtimestamp(cache_info.page_time)
            page_time_str = f"{page_datetime.year}-{page_datetime.month:02d}"
            if page_time_str in cache_group:
                cache_group[page_time_str].append(cache_info)
            else:
                cache_group[page_time_str] = [cache_info]
        for time_str in between_times:
            if time_str in cache_group:
                for style in style_list:
                    home_page_soup = init_home_page_content_element(style, time_str)
                    add_style(home_page_soup, style, "home_page_style_path")
                    save_page(home_page_soup, style.style_name, time_str, home_page_path)
                result.append(HomePageInfo(time_str, time_str, cache_group[time_str]))
    return result


def save_pdf(args):
    page_info, style_info = args
    content_file_names = [item.local_path for local_path in page_info.cache_infos for item in local_path.local_path_info
                          if item.style_name == style_info.style_name]
    pdf_file_path = merge_pdf(page_info.home_page_name, content_file_names, style_info.style_name,
                              page_info.home_page_name)
    out_pdf_path = pdf_file_path.rsplit('.', 1)[0] + "_add_page_number.pdf"
    add_page_numbers_with_outline(pdf_file_path, out_pdf_path, style_info)


def convert_to_pdf():
    args = []
    for page_info in page_infos:
        for style_info in style_list:
            args.append((page_info, style_info))

    with ProcessPoolExecutor() as executor:
        executor.map(save_pdf, args)


if __name__ == '__main__':
    logger.info("init begin")
    logger.debug(f"config is load config:{config}")
    logger.info(run_module)
    all_cache_infos = init_crawl_data()
    logger.info(f"all cache info :{all_cache_infos}")
    page_infos = []
    if grouping_rules == "month":
        page_infos = init_home_page_month_info()
    convert_to_pdf()
    logger.info("end ")
