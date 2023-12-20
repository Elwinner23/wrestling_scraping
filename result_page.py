from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re

driver = webdriver.Firefox()
excel_file_path = r'C:\Users\TARIEL\Desktop\wrestling_scraping\results.xlsx'
sheet_name = 'Sheet1'
column_name = 'page_link'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
column_data = df[column_name]
result_page_url = []
tournament_date_name = []
list_style = ["Freestyle", "Greco-Roman", "Women's wrestling"]
# driver.get('https://uww.org/event/klippan-lady-open-4/results')
time.sleep(2)
data = []
weight = []
countries =[]
# tabs_container = driver.find_element(By.CLASS_NAME, 'tabs-container')

def stage(count):
    tabs_container_wrap = driver.find_element(By.CLASS_NAME, 'tabs-container-wrap')
    for div in tabs_container_wrap.find_elements(By.CLASS_NAME, 'tabs-container-group'):
        title = div.find_element(By.TAG_NAME,'h3')
        content = div.find_element(By.CLASS_NAME,'tabs-container-content')
        for item in content.find_elements(By.CLASS_NAME,'content-item'):
            items = []
            content_wrapper = item.find_element(By.CLASS_NAME,'content-wrapper')
            card_content =content_wrapper.find_element(By.CLASS_NAME,'card-content')
            items.append(title.text)
            items.append(weight[count])
            for i in card_content.find_elements(By.CLASS_NAME,'card-item'):
                card_info = i.find_element(By.TAG_NAME,'span')
                items.append(card_info.text)
                img = i.find_element(By.CLASS_NAME,'logo')
                img_src = img.get_attribute('data-src')
                country = re.findall(r'/\w+/(\w+)\.png',img_src)
                countries.append(country[0])
                card_number = i.find_element(By.CLASS_NAME,'card-number')
                items.append(card_number.text)
            card_status = card_content.find_element(By.CLASS_NAME,'status')
            items.append(card_status.text)    
            data.append(items)

def get_filter_weight():
    count=0
    filter_label_group = driver.find_element(By.CLASS_NAME, 'filter-label-group')
    filter_ul = filter_label_group.find_element(By.TAG_NAME, 'ul')
    for li in filter_ul.find_elements(By.TAG_NAME, 'li'):
        span = li.find_element(By.TAG_NAME,'span')
        time.sleep(2)
        # Use try-except block to handle StaleElementReferenceException
        try:
            # Use ActionChains to perform the click action
            ActionChains(driver).move_to_element(li).click().perform()
            weight.append(span.text)
            time.sleep(1)
            stage(count)
            count+=1
        except StaleElementReferenceException:
            # If StaleElementReferenceException occurs, re-locate the element and retry
            li = filter_ul.find_element(By.TAG_NAME, 'li')
            ActionChains(driver).move_to_element(li).click().perform()
            weight.append(span.text)
            stage(count) 
            count+=1   

def get_filter_style():
    select_box = driver.find_element(By.CLASS_NAME, 'waf-select-box')
    select_box.click()
    select_list = select_box.find_element(By.CLASS_NAME, 'select-list')
    for li in select_list.find_elements(By.TAG_NAME, 'li'):
        button = li.find_element(By.TAG_NAME, 'button')
        if button.text in list_style:
            data.append(button.text)
            # Use try-except block to handle StaleElementReferenceException
            try:
                # Use ActionChains to perform the click action
                ActionChains(driver).move_to_element(button).click().perform()
                get_filter_weight()
            except StaleElementReferenceException:
                # If StaleElementReferenceException occurs, re-locate the element and retry
                button = select_list.find_element(By.TAG_NAME, 'button')
                ActionChains(driver).move_to_element(button).click().perform()
                get_filter_weight()
        select_box.click()
    select_box.click()


# get_filter_style()
# print(len(countries),countries,len(data))


def tournament_page():
    for i in column_data:
        if i.endswith('results'):
            result_page_url.append(i)
    return result_page_url

def open_tournament_page():
    pages = tournament_page()
    for page in pages:
        driver.get(page)
        driver.execute_script("window.scrollTo(0, 150)")
        time.sleep(2)
        get_filter_style()
        swiper_wrapper = driver.find_element(By.CLASS_NAME, 'swiper-wrapper')
        event_content_locator = swiper_wrapper.find_element(By.CLASS_NAME, 'event-content')
        venue_info = event_content_locator.find_element(By.CLASS_NAME,'venue-info')
        date = (venue_info.find_element(By.CLASS_NAME,'meta')).text
        name = (event_content_locator.find_element(By.TAG_NAME,'h3')).text
        tournament_date_name.append(date)
        tournament_date_name.append(name)
open_tournament_page()
