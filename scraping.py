from selenium import webdriver
from openpyxl import Workbook
from selenium.webdriver.common.by import By
import pandas as pd
import time 

driver = webdriver.Firefox()
url = 'https://uww.org/events'
driver.get(url)
years = ['2018', '2019', '2020', '2021', '2022']

#tournament_select = driver.find_element(By.CLASS_NAME, 'waf-select-box')
#tournament_select.click()
world_championship = driver.find_element(By.XPATH, '//*[@id="b26d198b-4b14-4220-b7bb-481ec09a8f1d"]/div/div/div[2]/div[1]/div/div[2]/div[1]/div[5]/div[1]/p[2][contains(text(), "2023")]')
world_championship.click()
select_list = world_championship.find_element(By.XPATH, '//*[@id="b26d198b-4b14-4220-b7bb-481ec09a8f1d"]/div/div/div[2]/div[1]/div/div[2]/div[1]/div[5]/div[2]/ul')
for li in select_list.find_elements(By.TAG_NAME, 'li'):
    button = li.find_element(By.TAG_NAME, 'button')
    if button.text in years:
        button.click()
time.sleep(2)

main_table = driver.find_element(By.CLASS_NAME,'table-responsive')
table_wrapper = main_table.find_element(By.CLASS_NAME,'table-wrapper')
element_table = table_wrapper.find_element(By.XPATH,'/html/body/div/div/div/div/main/section[4]/section[3]/div/div/div/div/section/div/div/div[2]/div[2]/div[1]')

# Within the table, find all elements with the class name 'event-title'

data = []
wb = Workbook()
ws = wb.active
for table_div in main_table.find_elements(By.CLASS_NAME,'table-body'):
    row = [item.text for item in table_div.find_elements(By.CLASS_NAME,'text')]
    data.append(row)
print(data)    
# wb.save('wrestling_data.xlsx')
