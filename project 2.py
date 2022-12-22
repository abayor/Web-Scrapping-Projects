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
from selenium.common.exceptions import ElementNotInteractableException
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
url = 'https://www.pararius.com/apartments/amsterdam'
#page= requests.get(url)

#page_content
#c search-list__item--listing
#search-list__item search-list__item--listing
browser.get(url)
search_results = browser.find_element(By.CLASS_NAME, 'page__content')
browser.find_element(By.ID, 'onetrust-accept-btn-handler').click()
soup = BeautifulSoup(search_results.get_attribute('innerHTML'), 'html.parser')
lists = soup.find_all('section', class_="listing-search-item--for-rent")
posts_html = [] 
to_stop = False

while not to_stop:
   
    try:
      search_results = browser.find_element(By.CLASS_NAME, 'page__wrapper--content')
      soup = BeautifulSoup(search_results.get_attribute('innerHTML'), 'html.parser')
      posts_html.extend(soup.find_all('section'))
      browser.execute_script('window.scrollTo(727,10048)')
      
      button_next = browser.find_element(By.XPATH, '//a[text()="Next"]')
      button_next.click()
      time.sleep(2.5)
    
        
    except NoSuchElementException:
        #to_stop = break
     to_stop = True
     print("ended")
      
print('Collected {0} listings'.format(len(posts_html)))

# clean up & organize records
housing_list = namedtuple('housing_list', ['title', 'location', 'price', 'square_area', 'room'])
housing = []
for list in posts_html:
       
        title = list.find('a', class_="listing-search-item__link--title").text.replace('\n', '')
        location = list.find('div', class_ = "listing-search-item__sub-title").text.replace('\n', '')
        price = list.find('div', class_ = "listing-search-item__price").text.replace('\n', '')
        square_area = list.find('li', class_="illustrated-features__item illustrated-features__item--surface-area").text.replace('\n', '')
        room = list.find('li', class_="illustrated-features__item illustrated-features__item--number-of-rooms").text.replace('\n', '')
        
        print(title[0])
        housing.append(housing_list(title, location, price,square_area,room))
    
   
    
df = pd.DataFrame(housing)
#df.to_csv(f' ({datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")}).csv', index=False)
#df['link'] = df.apply(lambda row: f'=HYPERLINK("{row["post_url"]}","Link")', axis=1)
df.to_excel(f'Housing({datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")}).xlsx', index=False)

