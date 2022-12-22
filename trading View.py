import os
import time
import datetime
from collections import namedtuple #use to organize text and field in a more organized format
import selenium.webdriver as webdriver #line 5-7 are default selenium library 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from bs4 import BeautifulSoup
import pandas as pd

import os
import time
import datetime
from collections import namedtuple
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
import pandas as pd
#import requests
from csv import writer

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
firefox_driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
firefox_service = Service(firefox_driver_path)
firefox_option = Options()
firefox_option.set_preference('general.useragent.override', user_agent)
browser = webdriver.Firefox(service=firefox_service, options=firefox_option)
browser.implicitly_wait(7)

# click a hyperlink
'''
url = ['https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/',
       'https://www.tradingview.com/markets/stocks-usa/market-movers-small-cap/',
       'https://www.tradingview.com/markets/stocks-usa/market-movers-largest-employers/',
       'https://www.tradingview.com/markets/stocks-usa/market-movers-high-dividend/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-highest-net-income/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-highest-cash/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-losers/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-active/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/'
       'https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-high/'
]
'''


urls = ['https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/',
       'https://www.tradingview.com/markets/stocks-usa/market-movers-largest-employers/']


for url in urls:
    browser.get(url)
    browser.maximize_window()
    categories = ['Overview', 'Performance', 'Valuation', 'Dividends', 'Margins', 'Income Statement', 'Balance Sheet', 'Oscillators', 'Trend-Following']
    
    #page= requests.get(url)

    #Set file base name
    file_name = url.split("/")[-2]
    print(f'Scrapping {url}...')
    #Excel Writer
    xlwriter = pd.ExcelWriter(file_name + '.xlsx')
    #Iterate Each reports on Trading View
    categories = ['Overview', 'Performance', 'Valuation', 'Dividends', 'Margins', 'Income Statement', 'Balance Sheet', 'Oscillators', 'Trend-Following']

    for category in categories:
        print(f'processing report:{category}')
        try:
            tab = browser.find_element(By.XPATH, f'//button[text()="{category}"]' )
            #tab = browser.find_element(By.LINK_TEXT, f'{category}' )
            #tab = browser.find_element(By.XPATH, f'//span[text()="{category}"]')
            #pass
            try:
                tab.click()
            except ElementNotInteractableException:
                pass
            time.sleep(3.5)
            df = pd.read_html(browser.page_source)[1]
            df.replace("-",'',inplace=False)
            df.to_excel(xlwriter, sheet_name=category, index=False)
            
        except (NoSuchElementException, TimeoutException):
            #tv-layout-width
            #class="square-tab-button-Tm9B6mdh square-tab-button-EprJANAf size-xsmall-Tm9B6mdh size-xsmall-EprJANAf"
            #id_market-screener-header-columnset-tabs_tablist
            print(f'Report {category} is not found')
            continue
    #df.to_excel(xlwriter, f'Trading({datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")}).xlsx', index=False)
    xlwriter.save()
browser.quit()

