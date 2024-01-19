from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
import db

driver = webdriver.Firefox()
excel_file_path = r'C:\Users\TARIEL\Desktop\wrestling_scraping\meeting.xlsx'
sheet_name = 'Sheet1'
column_name = 'links'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
column_data = df[column_name]
match_video_list = []
# driver.get("https://login.uww.org/uwwssodemo.onmicrosoft.com/b2c_1a_signup_signin/oauth2/v2.0/authorize?client_id=25b06501-7b83-4e13-95dc-077e0f42c6ab&scope=openid%20https%3A%2F%2Fuwwssodemo.onmicrosoft.com%2Fmobileapp%2Fdemo.read%20profile%20offline_access&redirect_uri=https%3A%2F%2Fuww.org&client-request-id=7c303ecb-a0a0-4aa9-b720-545d84401400&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.30.0&client_info=1&code_challenge=jQ7LyVAzOI12T_u8ZQRzYldIyUZN3rI-loGUrFaOZWc&code_challenge_method=S256&nonce=a1f52d6a-1806-49fd-9b51-de94bcd2b87c&state=eyJpZCI6IjQyMDYyOWE1LWM0MTktNDE3My1hNTVkLTZmNWFlNTE3MDEwNiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D")
def login():
    time.sleep(3)
    email = driver.find_element(By.ID, "signInName")
    password = driver.find_element(By.ID, "password")
    email.send_keys(db.email)
    password.send_keys(db.password)
    btn = driver.find_element(By.XPATH, '//*[@id="next"]')
    btn.click()
    time.sleep(2)
def get_data():
    for i in range(12898,12998):                    
        driver.get(column_data[i])
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 250)")
        login_btn = driver.find_element(By.XPATH,'/html/body/div/div/div/div/header/section/div/div[2]/nav/ul/li[7]/button')
        span_txt = login_btn.find_element(By.XPATH,'/html/body/div/div/div/div/header/section/div/div[2]/nav/ul/li[7]/button/span')
        text = span_txt.text
        if text == "LOG IN":
            login_btn.click()
            time.sleep(3)
            login()
            time.sleep(2)
        try:
            waf_body = driver.find_element(By.CLASS_NAME,'waf-body')
            content_wrapper = waf_body.find_element(By.CLASS_NAME,'content-wrapper')
            masthead_section =content_wrapper.find_element(By.CLASS_NAME,'masthead-section')   
            card_item = masthead_section.find_element(By.CLASS_NAME,'card-item') 
            content_wrap = content_wrapper.find_element(By.CLASS_NAME,'content-wrap') 
            tab_container_wrap = content_wrap.find_element(By.CLASS_NAME,'tab-container-wrap') 
            team_detail = tab_container_wrap.find_element(By.CLASS_NAME,'team-detail')
            team_a = team_detail.find_element(By.CLASS_NAME,'team-a')
            team_meta = team_a.find_element(By.CLASS_NAME,'team-meta')
            for li in team_meta.find_elements(By.CLASS_NAME,'meta'):
                age = li.text
            match_video_list.append(age)   
        except:
    
            match_video_list.append('no age') 
        try:
            card_footer = card_item.find_element(By.CLASS_NAME,'card-footer') 
            video_btn = card_footer.find_element(By.TAG_NAME,'a') 
            video_btn.click()
            time.sleep(2)
            site_common_wrapf = driver.find_element(By.CLASS_NAME,'site-common-wrap')
            data_section = site_common_wrapf.find_element(By.TAG_NAME,'div')
            modal_wrapper = data_section.find_element(By.CLASS_NAME,'modal-wrapper')
            modal_body = modal_wrapper.find_element(By.CLASS_NAME,'modal-body')
            close = modal_body.find_element(By.CLASS_NAME,'back-close')
            video_section = modal_body.find_element(By.CLASS_NAME,'video-section')
            embed_responsive = video_section.find_element(By.CLASS_NAME,'embed-responsive')
            iframe_ytb = embed_responsive.find_element(By.TAG_NAME,'iframe')
            ytbe_link = iframe_ytb.get_attribute('src')
            match_video_list.append(ytbe_link)
            close.click()
        except:
            match_video_list.append(driver.current_url)  
    return  match_video_list    
data = get_data()

def dataset(data):
    age = []
    match_video = []
    for x in range(len(match_video_list)):
        if x % 2 == 0:
            age.append(match_video_list[x])
        else:
            match_video.append(match_video_list[x])

    df = pd.DataFrame({'age' : age, 'match_video' : match_video})
    return df

df = dataset(data)
df.to_excel('data12900_13000.xlsx', index = False)

