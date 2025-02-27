import json
import os
import sys
import time

from loguru import logger

from spider_to_pdf.app_config import project_root, config_file_path, main_config

_cache_file = main_config.get("cache_file_name", ".cache.txt")
_cache_local_path = os.path.join(project_root, config_file_path, _cache_file)
_cache_local_tmp_path = os.path.join(project_root, config_file_path)

if not os.path.isfile(_cache_local_path):
    logger.error("cache file is not exists")
    try:
        with open(_cache_local_path, 'w') as file:
            pass
        logger.info("create cache file success")
    except Exception as e:
        logger.error(f"create cache file error e:{e.args}")
        sys.exit(1)


class LocalPathInfo:
    def __init__(self, style_name: str, local_path: str):
        self.style_name = style_name
        self.local_path = local_path

    @staticmethod
    def dict_to(obj: dict):
        return LocalPathInfo(obj["style_name"], obj["local_path"])

    def to_dict(self) -> dict:
        """ 将 PageInfo 对象转换为字典 """
        return {
            "style_name": self.style_name,
            "local_path": self.local_path
        }


class CacheInfo:
    def __init__(self, page_name: str, page_url: str = None, page_time: int = None,
                 local_path_info: list[LocalPathInfo] = None):
        self.page_name = page_name
        self.page_url = page_url
        self.page_time = page_time
        self.local_path_info = local_path_info if local_path_info is not None else []

    @staticmethod
    def dict_to(obj: dict):
        # 将字典转换为 CacheInfo 对象
        local_path_info = [LocalPathInfo.dict_to(item) for item in obj.get("local_path_info", [])]
        return CacheInfo(
            page_name=obj["page_name"],
            page_url=obj.get("page_url"),
            page_time=obj.get("page_time"),
            local_path_info=local_path_info
        )

    def to_dict(self) -> dict:
        """ 将 CacheInfo 对象转换为字典 """
        return {
            "page_name": self.page_name,
            "page_url": self.page_url,
            "page_time": self.page_time,
            "local_path_info": [info.to_dict() for info in self.local_path_info]
        }


def clean_all_cache():
    logger.info("clean cache file")
    tmp_cache_file_path = os.path.join(str(_cache_local_tmp_path), f"cache_{int(time.time())}.txt")
    with open(_cache_local_path, "r", encoding="UTF-8") as cache_file, open(tmp_cache_file_path, "w+",
                                                                            encoding="UTF-8") as cache_tmp_file:
        cache_tmp_file.write(cache_file.read())
    with open(_cache_local_path, "w", encoding="UTF-8") as cache_file:
        pass


def load_cache() -> list[CacheInfo]:
    logger.info("load cache.")
    result = []
    with open(_cache_local_path, "r", encoding="UTF-8") as cache_file:
        lines = cache_file.readlines()
        for line in lines:
            json_dict = json.loads(line)
            result.append(CacheInfo.dict_to(json_dict))
    logger.info(f"cache infos:{result}")
    return result


def update_cache(cache_infos: list[CacheInfo]) -> bool:
    logger.info(f"update cache cache_infos:{cache_infos}")
    if not cache_infos:
        return False
    with open(_cache_local_path, "w+", encoding="UTF-8") as cache_file:
        for cache_info in cache_infos:
            cache_file.write(json.dumps(cache_info.to_dict(), ensure_ascii=False))
            cache_file.write("\n")
    return True
