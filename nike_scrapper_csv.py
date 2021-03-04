from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import time

# Use ChromeDriveManager to open the webdriver to avoid version issues
driver = webdriver.Chrome(ChromeDriverManager().install())
# Go to the page that we want to scrape
driver.get("https://www.nike.com/w/mens-shoes-nik1zy7ok")

# Click on United States button to enter the desired country on the pop-up
close_button = driver.find_element_by_xpath('//a[@title="United States"]')
close_button.click()
time.sleep(2)

# Go back to the page that we want to scrape
driver.get("https://www.nike.com/w/mens-shoes-nik1zy7ok")

# # Script to scroll until infinite scroll ends to load all products on the page

# SCROLL_PAUSE_TIME = 1.5

# while True:

#     # Get scroll height
#     ### This is the difference. Moving this *inside* the loop
#     ### means that it checks if scrollTo is still scrolling 
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)

#     # Click on 'X' button to close news pop-up
#     try:
#     	close_button1 = driver.find_element_by_xpath('//button[@class="pre-modal-btn-close bg-transparent"]')
#     	close_button1.click()
#     except:
#     	pass

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:

#         # try again (can be removed)
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)

#         # Calculate new scroll height and compare with last scroll height
#         new_height = driver.execute_script("return document.body.scrollHeight")

#         # check if the page height has remained the same
#         if new_height == last_height:
#             # if so, you are done
#             break
#         # if not, move on to the next loop
#         else:
#             last_height = new_height
#             continue

# Click on 'X' button to close news pop-up
try:
	close_button1 = driver.find_element_by_xpath('//button[@class="pre-modal-btn-close bg-transparent"]')
	close_button1.click()
except:
	pass

# Getting a list of all the products on the page based on their XPATH
wait_product = WebDriverWait(driver, 10)
products = wait_product.until(EC.presence_of_all_elements_located((By.XPATH,
							'//a[@class="product-card__link-overlay"]')))

# Extract the URL from each of the products elements
urls = []
for product in products:
	url = product.get_attribute('href')
	urls.append(url)

# Looping through all products on the page
index = 1
for url in urls:

	# Initialize an empty dictionary for the data
	data_dict = {}

	# Click on 'X' button to close news pop-up
	try:
		close_button1 = driver.find_element_by_xpath('//button[@class="pre-modal-btn-close bg-transparent"]')
		close_button1.click()
	except:
		pass

	print("Scraping Product " + str(index))
	index = index + 1
	driver.get(url)
	title = driver.find_element_by_xpath('//h1[@id="pdp_product_title"]').get_attribute('textContent')
	category = driver.find_element_by_xpath('//h2[@class="headline-5-small pb1-sm d-sm-ib css-1ppcdci"]').get_attribute('textContent')
	price = driver.find_element_by_xpath('//div[@class="product-price is--current-price css-1emn094"]').get_attribute('textContent')
	description = driver.find_element_by_xpath('//div[@class="description-preview body-2 css-1pbvugb"]/p').get_attribute('textContent')
	description_long = driver.find_element_by_xpath('//div[@class="pi-pdpmainbody"]').get_attribute('textContent')
	print(description_long)


	# Go back to the previous page
	driver.execute_script("window.history.go(-1)")