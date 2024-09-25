from selenium import webdriver
from bs4 import BeautifulSoup as BS
from tqdm.auto import tqdm
import dotenv, time
import pandas as pd
import numpy as np

def get_flts(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(30)
    soup = BS(driver.page_source, 'lxml')
    return soup.find_all('ol', attrs={'class' : 'hJSA-list'})