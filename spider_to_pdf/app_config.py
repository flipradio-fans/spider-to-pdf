# -*- coding: utf-8 -*-
import os.path
import sys
from pathlib import Path

import yaml
from loguru import logger

# get project root dir
project_root = Path(__file__).parent.parent

# logs dir
config_dir = project_root / "config"

if not os.path.isdir(config_dir):
    logger.error("config dir not exits")
    raise ValueError("config is must.")

config_file_path = os.path.join(config_dir, "config.yaml")


def load_config():
    try:
        with open(config_file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError as e:
        logger.error("config file not found")
        sys.exit(1)


class Config:
    def __init__(self):
        logger.info("init config")
        self.config_data = load_config()

    def get(self, section, key=None):
        logger.debug(f" section:{section} ,key:{key}")
        if key is None:
            return self.config_data.get(section, {})
        return self.config_data.get(section, {}).get(key)

    def __str__(self):
        return str(self.config_data)


config = Config()
main_config = config.get("main")
main_argv = sys.argv
run_module = "test" if len(main_argv) > 1 and sys.argv[1:][0] == "test" else sys.argv[1:][0] if len(
    main_argv) > 1 else "product"

resource_path = main_config.get("resources_path")
config_file_path = main_config.get("cache_file_path", "tmp")
html_path = main_config.get("html_path")
home_page_path = main_config.get("home_page_path")
out_put_path = main_config.get("out_put_path")
grouping_rules = main_config.get("grouping_rules")
base_url = config.get("spider", "base_url")
