from selenium import webdriver
from bs4 import BeautifulSoup as BS
from tqdm.auto import tqdm
import dotenv, time
import pandas as pd
import numpy as np

def get_flts(url) -> list:
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(20)
    soup = BS(driver.page_source, 'lxml')
    return soup.find_all('div', attrs={'class' : 'nrc6-inner'})

def clean_flts(flts_list) -> pd.DataFrame:
    clnd_flts = []
    for flt in tqdm(flts_list, 'Cleaning Flights..', leave=False):
        spans = flt.findAll('span')
        airlines = flt.find_all('div', attrs={'dir' : 'auto'})
        prices = flt.find_all('div', attrs={'class' : 'f8F1-price-text'})
        cabins = flt.find_all('div', attrs={'class' : 'DOum-name DOum-mod-ellipsis'})
        href_list = list(set([x['href'] for x in flt.find_all('a', attrs={'class' : 'oVHK-fclink'})]))
        ob_stops = 0 if spans[6].getText() == 'nonstop' else int(spans[6].getText()[0])
        ob_offset = 0 if ob_stops == 0 else 2
        rtrn_stops = spans[17 + ob_offset].getText()
        rtrn_stops = 0 if rtrn_stops == 'nonstop' else int(rtrn_stops[0])
        rtrn_offset = ob_offset + 0 if rtrn_stops == 0 else ob_offset + 2
        if ob_stops > 1 or rtrn_stops > 1: pass
        for cabin in range(0, len(cabins)): 
            clnd_flts.append({
                'ob_dep_tm' : spans[3].getText()
                ,'ob_arr_tm' : spans[5].getText()
                ,'ob_airline' : airlines[0].getText().split(' ')[0]
                ,'ob_stops' : ob_stops
                ,'ob_orig_arpt' : spans[8 + ob_offset].getText()
                ,'ob_dest_arpt' : spans[11 + ob_offset].getText()
                ,'rtrn_dep_tm' : spans[14 + ob_offset].getText()
                ,'rtrn_arr_tm' : spans[16 + ob_offset].getText()
                ,'rtrn_airline' : airlines[1].getText().split(' ')[0]
                ,'rtrn_stops' : rtrn_stops
                ,'rtrn_orig_arpt' : spans[19 + rtrn_offset].getText()
                ,'rtrn_dest_arpt' : spans[22 + rtrn_offset].getText()
                ,'cabin' : cabins[cabin].getText()
                ,'fare' : prices[cabin].getText()
                ,'bkng_link' : f'https://www.kayak.com{href_list[cabin]}'
            })
    return pd.DataFrame(clnd_flts)