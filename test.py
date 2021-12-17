import json
import re 

from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.action_chains import ActionChains

def main():
    try:
        # build web driver 
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # get web content 
        driver.get('https://www.tesla.com/inventory/used/mx')
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'filter-zip'))
        )

        # select zip code 80205 (Denver)
        elem = driver.find_elements_by_id('filter-zip')[0]
        for i in range(5):
            elem.send_keys(Keys.BACK_SPACE)

        elem.send_keys(Keys.NUMPAD8)
        elem.send_keys(Keys.NUMPAD0)
        elem.send_keys(Keys.NUMPAD2)
        elem.send_keys(Keys.NUMPAD0)
        elem.send_keys(Keys.NUMPAD5)
        elem.send_keys(Keys.ENTER)

        # scrape indexed data
        photos = driver.find_elements_by_class_name('result-photos-main')
        cars = driver.find_elements_by_class_name('result-view-details-btn')

        # hover over picture to enable View Details button
        hover = ActionChains(driver).move_to_element(photos[0])
        hover.perform()

        # wait for View Details button to be clickable 
        WebDriverWait(driver, 500).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'result-view-details-btn'))
        )

        # click the button!
        cars[0].click()

        windows = driver.window_handles
        for window in windows:
            if window != driver.current_window_handle:
                driver.switch_to_window(window)


    
        # with open("page.html", "r") as page_file:
        #     page = BeautifulSoup(page_file, 'html.parser')

        page = BeautifulSoup(driver.page_source, 'html.parser')
        with open("page.html", "w") as page_file:
            page_file.write(page.prettify())

        # wait for new page to load 
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".idp--vehicle-trim.tds-text--300.tds-text--section_headline"))
        )

        h1 = page.findAll('div', {'class': 'idp--vehicle_header'})[0].findAll('h1')[0].text.split('\n')
        for i, item in enumerate(h1):
            print(f'{i}: {item}')
        vehicle = h1[1].strip()
        version = h1[3].strip()
    
        # wait for new page to load 
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".tds-text--body_small_headline"))
        )
        mileage = page.findAll('div', {'class': 'idp--vehicle_header'})[0].findAll('div', {'class': 'tds-text--body_small_headline'})[0].text.strip()
        location = page.findAll('div', {'class': 'idp--vehicle_header'})[0].findAll('div')[1].text.strip()[11:]

        # wait for new page to load 
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".idp--list_block.block-key_features"))
        )

        features = []
        li = page.findAll('div', {'class': ['idp--list_block', 'block-key_features']})[0].findAll('li', 'tds-list-item')
        for feature in li:
            features.append(feature.text.strip())

        print(f'Vehicle: {vehicle}')
        print(f'Version: {version}')
        print(f'Mileage: {mileage}')
        print(f'Location: {location}')
        for feature in features:
            print(f'Feature: {feature}')
 
        # import pdb; pdb.set_trace()
    except:
        print('error')
        raise 

    print('done')



if __name__ == '__main__':
    main()

    #a_string = '{ "name":"John", "age":30, "car":"None" }'
    #extract_json(a_string)