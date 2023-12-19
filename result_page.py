from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import pyautogui

driver = webdriver.Firefox()
excel_file_path = r'C:\Users\TARIEL\Desktop\wrestling_scraping\data.xlsx'
sheet_name = 'Sheet1'
column_name = 'page_link'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
column_data = df[column_name]
result_page_url = []
tournament_dates = []
list_style = ["Greco-Roman","Women's wrestling"]
driver.get('https://uww.org/event/granma-y-cerro-pelado-4/results')
time.sleep(2)
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
filter_label_group = driver.find_element(By.CLASS_NAME,'filter-label-group')
filter_ul = filter_label_group.find_element(By.TAG_NAME, 'ul')
tabs_container = driver.find_element(By.CLASS_NAME,'tabs-container')  
tabs_container_wrap = driver.find_element(By.CLASS_NAME,'tabs-container-wrap')
pages = []

def click_page():
    for div in tabs_container_wrap.find_elements(By.CLASS_NAME,'tabs-container-group'):
        content = div.find_element(By.CLASS_NAME,'tabs-container-content')
        waf_accordion_panel = content.find_element(By.CLASS_NAME,'waf-accordion-panel')
        content_item = waf_accordion_panel.find_element(By.CLASS_NAME,'content-item')
        element = content_item.find_element(By.CLASS_NAME, 'content-wrapper')
        action = element.find_element(By.CLASS_NAME,'card-action')
        a = action.find_element(By.TAG_NAME, 'a')
        link = a.get_attribute('href')
        pages.append(link)

          
def get_filter_weight():
    for li in filter_ul.find_elements(By.TAG_NAME, 'li'):
        li.click()
        click_page()
   
def get_filter_style():
    select_box = driver.find_element(By.CLASS_NAME,'waf-select-box')
    select_box.click()
    select_list = select_box.find_element(By.CLASS_NAME,'select-list')
    for li in select_list.find_elements(By.TAG_NAME, 'li'):
        button = li.find_element(By.TAG_NAME,'button')
        if button.text in list_style:
            print(button.text)
            button.click()
            time.sleep(2)
            get_filter_weight()
        select_box.click()            
    select_box.click() 
    
def tournament_page():
    for i in column_data:
        if i.endswith('results'):
            result_page_url.append(i)
    return result_page_url
get_filter_style()
print(pages,len(pages)) 

def open_tournament_page():
    pages = tournament_page()
    for page in pages:
        driver.get(page)
        time.sleep(2)
        get_filter_style()
        # tournament date
        swiper_wrapper = driver.find_element(By.CLASS_NAME, 'swiper-wrapper')
        event_content_locator = swiper_wrapper.find_element(By.CLASS_NAME, 'event-content')
        venue_info = event_content_locator.find_element(By.CLASS_NAME,'venue-info')
        date = (venue_info.find_element(By.CLASS_NAME,'meta')).text
        tournament_dates.append(date)

# open_tournament_page()