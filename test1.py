import os
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import pyperclip
import requests
import json
from csv import DictReader
from datetime import datetime
import random
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
op = Options()
# set .crx file path of extension
op.add_extension('cjpalhdlnbpafiamejdnhcphjbkeiagm.crx')

url = "https://www.imagetotext.info/"
save_directory = "H:\\My Drive\\Clone Macbook\\image to text"
# Replace 'path_to_webdriver' with the actual path to the web driver executable
driver = webdriver.Chrome('chromedriver.exe',
    options=op)
driver.minimize_window()
driver.get('https://www.imagetotext.info/login')
# enter username and password
username_field = driver.find_element_by_name('email')
#####Username imagetotext.info
username_field.send_keys('Username imagetotext.info')
password_field = driver.find_element_by_name('password')
#####password imagetotext.info

password_field.send_keys('#####password imagetotext.info')
password_field.send_keys(Keys.RETURN)

# wait for the page to load
time.sleep(5)
driver.get('https://www.imagetotext.info')


def to_title(string):
    regex = re.compile("[a-z]+('[a-z]+)?", re.I)
    return regex.sub(lambda grp: grp.group(0)[0].upper() + grp.group(0)[1:].lower(),
                     string)


def edit_text(input_text):
    new_text = input_text.replace('\n', ' ').replace('\r', '')
    new_text = new_text.replace('✩', ' ')
    new_text = new_text.replace('=', ' ')
    new_text = new_text.replace('  ', ' ')

    new_text = to_title(new_text)

    return new_text


def save_image_from_url(image_url, save_directory):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error downloading the image:", e)
        return

    # Get the filename from the URL
    filename = os.path.basename(image_url)

    # Combine the save directory and filename to get the full save path
    save_path = os.path.join(save_directory, filename)

    # Save the image to the specified directory
    try:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except IOError as e:
        print("Error saving the image:", e)
    else:
        print("Image saved successfully to:", save_path)
    return save_path


def click_browse_and_upload_file(file_path):

    try:
        # Wait for the page to load and the 'Browse' button to be clickable

        # browse_button = driver.find_element_by_class_name('browse-btn')
        browse_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "file"))
        )
        browse_button.send_keys(file_path)

        # # Click on the 'Browse' button to trigger the file upload dialog
        # browse_button.click()
        # time.sleep(2)
        # pyautogui.write(file_path)
        # pyautogui.press('enter')
        # submit_button = driver.find_element_by_id('jsShadowRoot')
        submit_button = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.ID, 'jsShadowRoot'))
        )

        submit_button.click()
        try:
            copy_button = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'span.tooltip.copy_tooltip0.d-flex'))
            )
            copy_button.click()
            text_image = pyperclip.paste()
        except TimeoutException:
            text_image = 'khong co text'
        # Optionally, you can clear the clipboard after capturing the data
        time.sleep(5)
        driver.get('https://www.imagetotext.info')
        return text_image

    except Exception as e:
        print("Error:", e)


df = pd.DataFrame(columns=['tieude', 'text'])
with open(r'file.csv',
          encoding='utf-8-sig') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        urls = row['checklinkanh']
        tieude = row['tieude']
        urls = re.findall(r'(https?://\S+)', urls)
        for url in urls:
            file_path = save_image_from_url(url, save_directory)
            text_excel = click_browse_and_upload_file(file_path)
            text_image_2 = edit_text(str(text_excel))
            print(text_image_2)

            df = df.append(
                dict(
                    tieude=str(tieude),
                    text=str(text_image_2),
                ),
                ignore_index=True)
        df.to_csv(r'read_text.csv',
                  encoding='utf-8-sig', index=False)

driver.quit()
