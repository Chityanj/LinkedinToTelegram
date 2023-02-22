
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pickle
import telegram
import lxml
import re
import datetime
import requests



api_key = ''
user_id = ''
bot = telegram.Bot(token=api_key)
 
# Creating a webdriver instance
driver = webdriver.Chrome("/home/chityanj/linkedin/scrape/chromedriver")
# This instance will be used to log into LinkedIn
 
# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")
 
# waiting for the page to load
time.sleep(5)
 
# entering username

username = driver.find_element(By.ID, 'username')
# In case of an error, try changing the element
# tag used here.
 
# Enter Your Email Address
username.send_keys("") 
 
# entering password
pword = driver.find_element(By.ID, "password")

pword.send_keys("")       
 

driver.find_element(By.XPATH,"//button[@type='submit']").click()

time.sleep(5)
driver.get("https://www.linkedin.com/jobs/search?keywords=software+NOT+marketing+intern+NOT+human+resources+intern+NOT+human+resources+intern&distance=25&geoId=102713980&f_E=1&origin=JOBS_HOME_SEARCH_CARDS&lipi=urn%3Ali%3Apage%3Ad_flagship3_job_home%3B4AVQJSTdTNGxeU%2BCFYu83A%3D%3D")
get_url = driver.current_url
url3 = get_url + "&sortBy=DD"
driver.get(url3)
time.sleep(2)
links = []


jobs_block = driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
for x in jobs_list:
    all_links = x.find_element(By.CLASS_NAME,'job-card-list__title')
    joblink = all_links.get_property('href') + "#" + all_links.text
    links.append(joblink)
    driver.execute_script("arguments[0].scrollIntoView();", x)
    time.sleep(1)

with open("/home/chityanj/linkedin/scrape/linkedin", "rb") as fp:   # Unpickling
    b = pickle.load(fp)
post = ''
for i in range(len(links)):
    if links[i] not in b:
        li,ti = links[i].split("#")
        loi = f'<a href="{li}">Link</a>'
        message = "Job Type: <b>Internship</b> " "\n" + 'Role: ' + ti + "\n" + 'Apply: ' + loi 
        
    post += message + "\n\n"
bot.send_message(chat_id=user_id, text=post, parse_mode='html')
print(post)
with open("/home/chityanj/linkedin/scrape/linkedin", "wb") as fp:   #Pickling
            pickle.dump(links, fp)


