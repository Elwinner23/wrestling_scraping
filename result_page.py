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
list_style = ["Freestyle", "Greco-Roman", "Women's wrestling"]
weight = []
countries = []
time.sleep(2)
# driver.get('https://uww.org/event/african-championships-0/results')
# driver.execute_script("window.scrollTo(0, 150)")
# swiper_wrapper = driver.find_element(By.CLASS_NAME, 'swiper-wrapper')
# event_content_locator = swiper_wrapper.find_element(By.CLASS_NAME, 'event-content')
# venue_info = event_content_locator.find_element(By.CLASS_NAME,'venue-info')
# date = (venue_info.find_element(By.CLASS_NAME,'meta')).text
# name = (event_content_locator.find_element(By.TAG_NAME,'h3')).text
    
def stage(count,data,countries,index,weight,styles):
    tabs_container_wrap = driver.find_element(By.CLASS_NAME, 'tabs-container-wrap')
    for div in tabs_container_wrap.find_elements(By.CLASS_NAME, 'tabs-container-group'):
        title = div.find_element(By.TAG_NAME,'h3')
        content = div.find_element(By.CLASS_NAME,'tabs-container-content')
        for item in content.find_elements(By.CLASS_NAME,'content-item'):
            items = []
            content_wrapper = item.find_element(By.CLASS_NAME,'content-wrapper')
            card_content =content_wrapper.find_element(By.CLASS_NAME,'card-content')
            items.append(styles[index])
            items.append(title.text)
            items.append(weight[count])
            items.append(date)
            items.append(name)
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
            if items not in data:    
                data.append(items)

def get_filter_weight(data,countries,index,count,weight,styles):
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
            stage(count,data,countries,index,weight,styles)
            count+=1
        except StaleElementReferenceException:
            # If StaleElementReferenceException occurs, re-locate the element and retry
            li = filter_ul.find_element(By.TAG_NAME, 'li')
            ActionChains(driver).move_to_element(li).click().perform()
            weight.append(span.text)
            stage(count,data,countries,index,weight,styles) 
            count+=1   

def get_filter_style():
    index =0
    count =0
    select_box = driver.find_element(By.CLASS_NAME, 'waf-select-box')
    select_box.click()
    select_list = select_box.find_element(By.CLASS_NAME, 'select-list')
    styles =[]
    data = []  # Initialize the data list
    countries = []  # Initialize the countries list
    for li in select_list.find_elements(By.TAG_NAME, 'li'):
        button = li.find_element(By.TAG_NAME, 'button')
        if button.text in list_style:
            styles.append(button.text)
            
            # Use try-except block to handle StaleElementReferenceException
            try:
                # Use ActionChains to perform the click action
                ActionChains(driver).move_to_element(button).click().perform()
                weight = []
                get_filter_weight(data, countries,index,count,weight,styles)
                index +=1
            except StaleElementReferenceException:
                # If StaleElementReferenceException occurs, re-locate the element and retry
                button = select_list.find_element(By.TAG_NAME, 'button')
                ActionChains(driver).move_to_element(button).click().perform()
                weight = []
                get_filter_weight(data, countries,index,count,weight,styles)
                index +=1
        select_box.click()        
    select_box.click()
    return data, countries

def meetings_table(df, country_list):
    style = []
    stage = []
    weight = []
    opponent1 = []
    opponent1_points = []
    opponent2 = []
    opponent2_points = []
    decision = []
    opponent1_country = []
    opponent2_country = []
    tournament_date = []
    tournament_name = []
    for x in range(len(country_list)):
        if x % 2 == 0:
            opponent1_country.append(country_list[x])
        else:
            opponent2_country.append(country_list[x])

    for i in range(len(df)):
        style.append(df[i][0])
        stage.append(df[i][1])
        weight.append(df[i][2])
        opponent1.append(df[i][5])
        opponent1_points.append(df[i][6])
        opponent2.append(df[i][7])
        opponent2_points.append(df[i][8])
        decision.append(df[i][9])
        tournament_date.append(df[i][3])
        tournament_name.append(df[i][4])
           
    print(df,len(style),len(stage),len(weight),len(opponent1),len(opponent2),len(tournament_name),len(tournament_date),len(opponent1_country),
          len(opponent2_country),len(opponent1_points),len(opponent2_points),len(decision))
    final_df = pd.DataFrame({'tournament_name': tournament_name,'tournament_date': tournament_date,
                             'style' : style, 'stage' : stage, 'weight' : weight, 'opponent1' : opponent1,
                             'opponent1_country': opponent1_country,
                             'opponent1_points' : opponent1_points,'opponent2_points' : opponent2_points,
                             'opponent2' : opponent2,'opponent2_country': opponent2_country,
                             'decision' : decision})
    return final_df

# df_data, countries_data = get_filter_style()  # Get the returned data and countries
# df = meetings_table(df_data, countries_data)     
# df.to_excel('meeting2.xlsx', index = False)
final_dataframe =pd.DataFrame(columns = ['tournament_name','tournament_date',
                             'style' , 'stage', 'weight', 'opponent1',
                             'opponent1_country',
                             'opponent1_points','opponent2_points',
                             'opponent2','opponent2_country',
                             'decision'])
for i in range(7,9):
    driver.get(column_data[i])
    driver.execute_script("window.scrollTo(0, 250)")
    swiper_wrapper = driver.find_element(By.CLASS_NAME, 'swiper-wrapper')
    event_content_locator = swiper_wrapper.find_element(By.CLASS_NAME, 'event-content')
    venue_info = event_content_locator.find_element(By.CLASS_NAME,'venue-info')
    date = (venue_info.find_element(By.CLASS_NAME,'meta')).text
    name = (event_content_locator.find_element(By.TAG_NAME,'h3')).text
    df_data, countries_data = get_filter_style()  # Get the returned data and countries
    df = meetings_table(df_data, countries_data) 
    final_dataframe = pd.concat([final_dataframe,df],axis=0)
final_dataframe.to_excel('meeting7_9.xlsx', index = False)
       