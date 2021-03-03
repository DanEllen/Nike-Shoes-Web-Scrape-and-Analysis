from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

# Use ChromeDriveManager to open the webdriver to avoid version issues
driver = webdriver.Chrome(ChromeDriverManager().install())
# Go to the page that we want to scrape
driver.get("https://www.nike.com/w/mens-shoes-nik1zy7ok")

#Click on 'X' button to close country pop-up
close_button = driver.find_element_by_xpath('//button[@class="hf-modal-btn-close"]')
close_button.click()


# Go back to the previous page
#driver.execute_script("window.history.go(-1)")

#Getting a list of all the products on the page based on their XPATH
index = 1
wait_product = WebDriverWait(driver, 10)
products = wait_product.until(EC.presence_of_all_elements_located((By.XPATH,
							'//a[@class="product-card__link-overlay"]')))

#Looping through all products on the page
for product in products:
	print(product)
	# print("Scraping Product " + str(index))
	# index = index + 1
	# url = product.get_attribute('href')
	# wait_button = WebDriverWait(driver, 10)
	# next_button = wait_button.driver.get(url)