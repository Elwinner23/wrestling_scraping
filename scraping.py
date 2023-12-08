import os

from selenium import webdriver
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