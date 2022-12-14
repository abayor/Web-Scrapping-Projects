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
from bs4 import BeautifulSoup
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
firefox_driver_path = os.path.join(os.getcwd(), 'geckodriver.exe')
firefox_service = Service(firefox_driver_path)
firefox_option = Options()
firefox_option.set_preference('general.useragent.override', user_agent)
browser = webdriver.Firefox(service=firefox_service, options=firefox_option)
browser.implicitly_wait(7)

# click a hyperlink
url = 'https://www.imdb.com/'
browser.get(url)


#IMBD menu
menu_dropdown =browser.find_element(By.ID, 'iconContext-menu')
menu_dropdown.click()

#Select Top 250 Movies
#Top_250 = browser.find_element(By.CLASS_NAME, 'ipc-list__item nav-link sc-fodVxV cYLuAZ ipc-list__item--indent-one')
Top_250 = browser.find_element(By.XPATH, "//a[@href='/chart/top/?ref_=nv_mv_250']")
Top_250.click()
##Now we'ere in the Top 250 movies Page
#Select_Top.select_by_visible_text('Top 250 Movies')

#Scrap the page
#Rank & Title
#IMBd Rating
#year


# store listings into a CSV and Excel file
posts_html = []
to_stop = False


while not to_stop:
    search_results = browser.find_element(By.CLASS_NAME, 'lister-list')
    soup = BeautifulSoup(search_results.get_attribute('innerHTML'), 'html.parser') 
    posts_html.extend(soup.find_all('tr'))
    #print(len(soup.find_all('tr')))
    to_stop = True

print('Collected {0} listings'.format(len(posts_html)))
#print(posts_html)
#Movie title
#year
#rating

# clean up & organize records
movie_rating = namedtuple('movie_rating', ['title', 'year', 'rating'])
#imbd = namedtuple('imbd', ['title', 'price', 'post_timestamp', 'location', 'post_url', 'image_url'])
movie_rate = []
for post_html in posts_html:
    #post_url = post_html.find('a', 'result-title').get('href')
    title = post_html.find('td', class_ = 'titleColumn').text
    year = post_html.find('span', 'secondaryInfo').text
    rating = post_html.find('td', class_='ratingColumn imdbRating').text
    
    
    
   # location = post_html.find('span', 'result-hood').text.replace('(', '').replace(')', '')
   # post_url = post_html.find('a', 'result-title').get('href')
    #image_url = post_html.find('img').get('src') if post_html.find('img') else ''
    print(title[0])
    movie_rate.append(movie_rating(title, year, rating))

df = pd.DataFrame(movie_rate)
#df.to_csv(f' ({datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")}).csv', index=False)

#df['link'] = df.apply(lambda row: f'=HYPERLINK("{row["post_url"]}","Link")', axis=1)
df.to_excel(f'({datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")}).xlsx', index=False)

browser.close()
#for_sale_element = browser.find_element(By.XPATH, "//a[@data-alltitle='all for sale']")

#select from dropdown (by displayed text)
# dropdown_neighborhood = browser.find_element(By.ID, 'subArea')
# select_neighrborhood = Select(dropdown_neighborhood)
# select_neighrborhood.select_by_visible_text('city of chicago')
# print(for_sale_element.text)
# print(for_sale_element.location)
# print(for_sale_element.is_enabled())

# # select from dropdown (by displayed text)
# dropdown_neighborhood = browser.find_element(By.ID, 'subArea')
# select_neighrborhood = Select(dropdown_neighborhood)
# select_neighrborhood.select_by_visible_text('city of chicago')

# # select from dropdown (by index position)
# dropdown_neighborhood = browser.find_element(By.ID, 'subArea')
# select_neighrborhood = Select(dropdown_neighborhood)
# select_neighrborhood.select_by_index(5)

# select from dropdown (by index position)
