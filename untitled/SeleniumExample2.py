from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from objectrepositoy.elementlocators import *
import time

# get current dir path
current_dir = os.getcwd()

# add chromedriver path with current directory
chrome_driver_path = current_dir + '/chromedriver_linux/chromedriver'

# create chrome session
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# maximize chrome
driver.maximize_window()
wait = WebDriverWait(driver, 60)

# bnavigate to sothebyshome website
driver.get("https://sothebyshome.com/")

# wait for popup and close
wait.until(EC.presence_of_element_located((By.XPATH, close_button_xpath)))
driver.find_element_by_xpath(close_button_xpath).click()


# check product count on one page and total count displayed at top
def check_product_count():
    wait.until(EC.presence_of_element_located((By.XPATH, product_count_xpath)))
    item_count = driver.find_element_by_xpath(product_count_xpath).text.split(" ")[0]
    wait.until(EC.presence_of_element_located((By.XPATH, product_grid_xpath)))
    grid_count = len(driver.find_elements_by_xpath(product_grid_xpath))
    if int(item_count) > 0 and grid_count > 0:
        print("PASS")
    else:
        print("FAIL")


# iterate through each menu and sub menu
nav_item_list = driver.find_elements_by_xpath(nav_item_xpath)
for i in range(0, len(nav_item_list) - 1):
    nav_item_list_new = driver.find_elements_by_xpath(nav_item_xpath)
    ActionChains(driver).move_to_element(nav_item_list_new[i]).perform()
    submenu_item_list_new = driver.find_elements_by_xpath(nav_item_submenu_xpath)
    submenu_data = submenu_item_list_new[i].text.split("\n")
    for data in submenu_data:
        print("====================")
        nav_item_list_temp = driver.find_elements_by_xpath(nav_item_xpath)
        print("Check " + data)
        ActionChains(driver).move_to_element(nav_item_list_temp[i]).perform()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, data)))
        link_element = driver.find_element_by_link_text(data)
        href_data = link_element.get_attribute('href')
        # continue if link is not clickakle and mark as NA
        try:
            if href_data[-1] == "#":
                print("NA")
                continue
        except Exception:
            print("FAIL")
            continue
        link_element.click()
        # mark fail if product grid and total count not present
        try:
            check_product_count()
        except Exception:
            print("FAIL")

            # navigate back to home page
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)

# close window and quit driver
driver.quit()
