import logging
import pymongo  # type: ignore
from python_log_indenter import IndentedLoggerAdapter # type: ignore
from selenium import webdriver  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from helpers.setup import log
from os import environ

log.info("Installing Selenium Chromedriver...")
environ["WDM_LOG_LEVEL"] = str(logging.WARNING)
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
log.info("Done")