from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
import time
import csv
import re

# Use ChromeDriveManager to open the webdriver to avoid version issues
driver = webdriver.Chrome(ChromeDriverManager().install())
# Go to the page that we want to scrape
driver.get("https://www.nike.com/w/mens-shoes-nik1zy7")

# Click on United States button to enter the desired country on the pop-up
close_button = driver.find_element_by_xpath('//a[@title="United States"]')
close_button.click()
time.sleep(2)

# Go back to the page that we want to scrape
#driver.get("https://www.nike.com/w/mens-shoes-nik1zy7ok?sort=newest")
driver.get("https://www.nike.com/w/mens-shoes-nik1zy7ok")

# Csv file we will use to store data
csv_file = open('nike_shoes.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

# # Script to scroll until infinite scroll ends to load all products on the page

# SCROLL_PAUSE_TIME = 1.0

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
#       close_button1 = driver.find_element_by_xpath('//button[@class="pre-modal-btn-close bg-transparent"]')
#       close_button1.click()
#     except:
#       pass

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
products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,
                            '//a[@class="product-card__link-overlay"]')))

# Extract the URL from each of the products elements
urls = []
for product in products:
    url = product.get_attribute('href')
    urls.append(url)

# Looping through all products on the page
index = 1
for url in urls[4:8]:

    # Initialize an empty dictionary for the data
    product_dict = {}

    # Click on 'X' button to close news pop-up
    try:
        close_button1 = driver.find_element_by_xpath('//button[@class="pre-modal-btn-close bg-transparent"]')
        close_button1.click()
    except:
        pass

    print("Scraping Product " + str(index))
    print(url)
    index = index + 1
    driver.get(url)
    id_ = index
    title = driver.find_element_by_xpath('//h1[@id="pdp_product_title"]').get_attribute('textContent')
    category = driver.find_element_by_xpath('//h2[@class="headline-5-small pb1-sm d-sm-ib css-1ppcdci"]').get_attribute('textContent')
    price = driver.find_element_by_xpath('//div[@class="product-price is--current-price css-1emn094"]').get_attribute('textContent')
    price = int(re.findall('\d+', price)[0])
    description = driver.find_element_by_xpath('//div[@class="description-preview body-2 css-1pbvugb"]/p').get_attribute('textContent')
    description_long = driver.find_element_by_xpath('//div[@class="pi-pdpmainbody"]').get_attribute('textContent')

    # Try to click review button and more button if it fails to find xpath put review as empty
    try:
        review_button = driver.find_element_by_xpath("(//button[@class='css-1y5ubft panel-controls'])[2]")
        review_button.click()
        time.sleep(1)
        try:
            more_button = driver.find_element_by_xpath('//label[@for="More Reviews"]')
            more_button.click()
            try:

                # Get average score for product
                score = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                            "//span[@class='TTavgRate']"))).get_attribute('textContent')
                score = re.findall("\d+\.\d+", score)[0]

                # Get the slider information
                sliders = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,
                            '//div[@class="TT4reviewRangeDot"]')))[:3]
                slider_data = [slider.get_attribute('style') for slider in sliders]
                slider_data = [float(re.search('margin-left: calc\((.+)% - 5px\);', slider).group(1)) for slider in slider_data]

                try:
                    # 0 Runs Small - 100 Runs Big
                    size = slider_data[0]
                    # 0 Uncomfortable - 100 Comfortable
                    comfort = slider_data[1]
                    # 0 Not Durable - 100 Durable
                    durability = slider_data[2]

                except Exception as e:
                    size = ""
                    comfort = ""
                    durability = ""

                # Getting number of reviews to know how many times to click load more reviews
                number_reviews = driver.find_element_by_xpath('//div[@class="TTreviewCount"]').get_attribute('textContent')
                number_reviews = float((re.findall(("\d+.\d+|\d+"), number_reviews)[0]).replace(",", ""))
                reviews_per_click = 20
                times = (number_reviews // reviews_per_click) + 1
                print("There are ", number_reviews, "reviews")
                print("Clicking load more", times, "times")
                index1 = 0
                # Loop to click load more, using .execute_script function because button is hidden
                while index1 < times:
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        load_more = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                            '//span[text()="Load More"]/..')))
                        driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(0.1)
                        index1 += 1
                    except Exception as e:
                        print(type(e), e)
                        print(url)
                        break

                # Getting a list of all the reviews to loop through            
                reviews = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,
                            '//div[@class="TTreview"]')))

                for count, review in enumerate(reviews):

                    r_title = review.find_element_by_xpath('.//div[@class="TTreviewTitle"]').get_attribute('textContent')
                    r_raiting = float(review.find_element_by_xpath('.//meta[@itemprop="ratingValue"]').get_attribute('content'))
                    r_body = review.find_element_by_xpath('.//div[@class="TTreviewBody"]').get_attribute('textContent')
                    r_date = review.find_element_by_xpath('.//div[@itemprop="dateCreated"]').get_attribute('datetime')
                    r_date = dt.datetime.strptime(r_date, '%Y-%m-%d')

                    product_dict['id_'] = id_
                    product_dict['title'] = title
                    product_dict['category'] = category
                    product_dict['price'] = price
                    product_dict['description'] = description
                    product_dict['description_long'] = description_long
                    product_dict['r_title'] = r_title
                    product_dict['r_raiting'] = r_raiting
                    product_dict['r_body'] = r_body
                    product_dict['r_date'] = r_date

                    writer.writerow(product_dict.values())

                print("Scrapped ", count+1, "reviews")

            except:
                review = ""
                score = ""
        except:
            review = ""
            score = ""
    except:
        review = ""
        score = ""
        product_dict['id_'] = id_
        product_dict['title'] = title
        product_dict['category'] = category
        product_dict['price'] = price
        product_dict['description'] = description
        product_dict['description_long'] = description_long
        product_dict['r_title'] = r_title
        product_dict['r_raiting'] = r_raiting
        product_dict['r_body'] = r_body
        product_dict['r_date'] = r_date

csv_file.close()
driver.close()