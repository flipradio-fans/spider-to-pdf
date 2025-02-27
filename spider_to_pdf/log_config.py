# -*- coding: utf-8 -*-

from loguru import logger

from spider_to_pdf.app_config import run_module, project_root

# logs dir
logs_dir = project_root / "logs"

# mkdir log dir
logs_dir.mkdir(parents=True, exist_ok=True)

# log file
log_file = logs_dir / "app.log"

if run_module == "product":
    # format log content
    logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss} | {level} |  {message}", level="INFO", rotation="1 MB")
if run_module == "test":
    logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {line} - {message}", level="DEBUG",
               rotation="1 MB")
if run_module == "dev":
    logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {line} - {message}",
               level="DEBUG", rotation="1 MB")
