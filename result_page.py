from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Firefox()
excel_file_path = r'C:\Users\TARIEL\Desktop\wrestling_scraping\data.xlsx'
sheet_name = 'Sheet1'
column_name = 'page_link'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
column_data = df[column_name]
result_page_url = []
tournament_dates = []
list_style = ['Freestyle','Greco-Roman',"Women's wrestling"]

def get_filter_style():
    select_box = driver.find_element(By.CLASS_NAME,'waf-select-box')
    select_box.click()
    select_list = select_box.find_element(By.CLASS_NAME,'select-list')
    for li in select_list.find_elements(By.TAG_NAME, 'li'):
        button = li.find_element(By.TAG_NAME,'button')
        if button.text in list_style:
            button.click()
        select_box.click()            
    select_box.click() 
def tournament_page():
    for i in column_data:
        if i.endswith('results'):
            result_page_url.append(i)
    return result_page_url

driver.get('https://uww.org/event/granma-y-cerro-pelado-4/results')
get_filter_style()
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
