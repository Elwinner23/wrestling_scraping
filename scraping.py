from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time 

driver = webdriver.Firefox()
url = 'https://uww.org/events'
driver.get(url)
years = ['2018', '2019', '2020', '2021', '2022']
year = []
data = []
page_link = []
# tournament_select = driver.find_element(By.CLASS_NAME, 'waf-select-box')
# tournament_select.click()
main_table = driver.find_element(By.CLASS_NAME,'table-responsive')
table_wrapper = main_table.find_element(By.CLASS_NAME,'table-wrapper')
element_table = table_wrapper.find_element(By.XPATH,'/html/body/div/div/div/div/main/section[4]/section[3]/div/div/div/div/section/div/div/div[2]/div[2]/div[1]')
world_championship = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/section[4]/section[3]/div/div/div/div/section/div/div/div[2]/div[1]/div/div[2]/div[1]/div[5]')
world_championship.click()
select_list = world_championship.find_element(By.CLASS_NAME,'select-list')
count=0
for li in select_list.find_elements(By.TAG_NAME, 'li'):
    button = li.find_element(By.TAG_NAME, 'button')
    if button.text in years:
      button.click()
      # web sehfeden datanin liste elave edilmesi
      for table_div in main_table.find_elements(By.CLASS_NAME,'table-body'):
            row = [item.text for item in table_div.find_elements(By.CLASS_NAME,'text')]
            data.append(row) 
        # Video linklerin liste yigilmasi       
      for a in driver.find_elements(By.CLASS_NAME,'table-row'):
            link = a.get_attribute('href')
            if link == None:
                continue
            else:
                page_link.append(link)
                year.append(years[count])
      count+=1    
    world_championship.click()

              



# Within the table, find all elements with the class name 'event-title'
# wb = Workbook()
# ws = wb.active

# wb.save('wrestling_data.xlsx')
# var olan datani tek-tek listlere ayirmaq   
chunks = []
def split_list(chunk_size):
    for i in range(0,len(data)):
        for j in range(0, len(data[i]), chunk_size):
            chunk = data[i][j:j + chunk_size]
            chunks.append(chunk)
    return chunks

chunk_size = 5
# print(page_link)

# def tournament_page(url):
#     driver.get(url)
# print(len(page_link),len(year),len(data),len(chunks))


def dataset(pl,yr):
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
    df = pd.DataFrame({'tournament_name' : tournament_name, 'location' : location, 'type' : type, 'age' : age, 'style' : style, 'page_link' : pl, 'year' : yr})
    return df

df = dataset(page_link,year)
df.to_excel('data.xlsx', index = False)