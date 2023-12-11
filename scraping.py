import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

os.environ['PATH'] += r'C:\MozilaDrivers'
years = ['2018', '2019', '2020', '2021', '2022']
driver = webdriver.Firefox()
driver.get('https://uww.org/events')
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
video_link = []

for table_div in main_table.find_elements(By.CLASS_NAME,'table-body'):
    row = [item.text for item in table_div.find_elements(By.CLASS_NAME,'text')]
    data.append(row) 
# elem = driver.find_element(By.CLASS_NAME,'table-body')
# link = elem[0].get_attribute('href')    
        
# wb.save('wrestling_data.xlsx')
    
def split_list(chunk_size):
    chunks = []
    for i in range(0,len(data)):
        for j in range(0, len(data[i]), chunk_size):
            chunk = data[i][j:j + chunk_size]
            chunks.append(chunk)
    return chunks

chunk_size = 5
def dataset():
    tournament_name = []
    location = []
    type = []
    age = []
    style = []
    data_read = split_list(chunk_size)
    for data in data_read:
        tournament_name.append(data[0])
        location.append(data[1])
        type.append(data[2])
        age.append(data[3])
        style.append(data[4])
    df = pd.DataFrame({'tournament_name' : tournament_name, 'location' : location, 'type' : type, 'age' : age, 'style' : style})
    return df

df = dataset()
print(df.head())