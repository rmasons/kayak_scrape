from selenium import webdriver
from bs4 import BeautifulSoup as BS
from tqdm.auto import tqdm
import dotenv, time
import pandas as pd
import numpy as np

def get_flts(url):
    driver = webdriver.Chrome()
    time.sleep(10)
    driver.get(url)
    soup = BS(driver.page_source, 'lxml')
    return soup