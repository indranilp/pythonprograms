from selenium import  webdriver
from selenium.webdriver.common.by import by
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import EC

driver = webdriver.Chrome("/home/indranil/Downloads/chromedriver")

driver.maximize_window()

driver.get("https://www.google.com/")

search_box = driver.find_element_by_xpath("//input[@name='q']")
wait = We
search_box.send_keys("hello")

driver.quit()