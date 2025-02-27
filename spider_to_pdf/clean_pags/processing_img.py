# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from loguru import logger

from spider_to_pdf.app_config import base_url, project_root, resource_path
from spider_to_pdf.app_config import config

_clean_config = config.get("clean")

_img_config = _clean_config.get("img_info", {})

if base_url is None:
    logger.error("base url is must")
    sys.exit(1)
_img_local_path = _img_config.get("img_local_path", "images")
_images_path: str = os.path.join(str(project_root), resource_path, _img_local_path)

if not os.path.isdir(_images_path):
    logger.error("_images_path dir not exits")
    try:
        os.makedirs(_images_path, )
        logger.info("created _images_path dir")
    except Exception as e:
        logger.error(f"_image_path create failed e:{e.args}")
        sys.exit(1)


def create_image_local_path(image_name: str) -> str:
    return os.path.join("..", "..", _img_local_path, image_name)


def download_image(image_url, retry_number: int = 0):
    """
    download image
    :param retry_number:  retry download number
    :param image_url: image url
    :return: if there isn't error return image local path else return image url
    """
    if retry_number == _img_config.get("max_retry_number", 3):
        return image_url
    image_name = os.path.basename(urlparse(image_url).path)
    image_path = os.path.join(str(_images_path), image_name)
    if os.path.exists(image_path):
        return create_image_local_path(image_name)
    try:
        response = requests.get(image_url)
        sleep(1)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                file.write(response.content)
                logger.debug(f"download img success image_path:{image_path}")
            return create_image_local_path(image_name)  # return local path
        else:
            logger.error(f"download img error image_url:{image_url}")
            return image_url  # return img url
    except Exception as exception:
        logger.error(f"download failed: {image_url} {exception.args} retry_number:{retry_number}")
        return download_image(image_url, retry_number + 1)


def processing_ghost_blog_html_img(html_info: BeautifulSoup) -> BeautifulSoup | None:
    """
    process ghost blog title img download img to local
    :param html_info:
    :return:
    """
    img_select = _img_config.get("img_select")
    if not img_select:
        logger.error("img select config is None")
        return None
    for select in img_select:
        img = html_info.select_one(select)
        if not img:
            return html_info
        if "src" in img.attrs and img["src"].startswith("/"):
            img_url = base_url + img["src"]
            img_local_path = download_image(img_url)
            img["src"] = img_local_path
        clean_img_attr = _img_config.get("clean_img_attr", [])
        for clean_attr in clean_img_attr:
            if clean_attr in img.attrs:
                img.attrs.pop(clean_attr)
    return html_info
