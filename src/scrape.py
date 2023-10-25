from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv

# Infatuation URL
infatuation_url = 'https://www.theinfatuation.com/new-york/reviews?page='
# NY Times URL
nytimes_url = 'https://www.nytimes.com/reviews/dining'
archive_site = 'https://archive.is/'
# Michelin URL
michelin_url = 'https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/page/'

# Output data
data = [
    ['restaurant_name', 'restaurant_cuisine', 'restaurant_cost', 'restaurant_location', 'review_rating', 'review_text', 'review_date', 'review_url'],
]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Scraping Infatuation
page_index = 1
restaurant_count = 0

while True:
    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.get(infatuation_url + str(page_index))
    restaurants = chrome_driver.find_elements(By.CLASS_NAME, 'css-10n1vic')
    
    if len(restaurants) == 0:
        break
    
    for restaurant in restaurants:
        restaurant_count += 1
        # print(restaurant_count)
        
        try:
            review_url_section = restaurant.find_element(By.CLASS_NAME, 'css-mm52m8')
            review_url = review_url_section.get_attribute('href')
            # print(review_url)
        except:
            break
        
        chrome_driver1 = webdriver.Chrome(options=chrome_options)
        chrome_driver1.get(review_url)
        
        try:
            restaurant_name = chrome_driver1.find_element(By.CLASS_NAME, 'css-67umdg').text
            # print(restaurant_name)
        except:
            restaurant_name = ""
        
        try:
            restaurant_cuisine_section = chrome_driver1.find_element(By.CLASS_NAME, 'cuisineTag')
            restaurant_cuisine = restaurant_cuisine_section.find_element(By.TAG_NAME, 'a').text
            # print(restaurant_cuisine)
        except:
            restaurant_cuisine = ""
        
        try:
            restaurant_cost_section = chrome_driver1.find_element(By.CLASS_NAME, 'css-utujt7')
            restaurant_cost_characters = restaurant_cost_section.find_elements(By.CLASS_NAME, 'css-1oehroq')
            restaurant_cost = '$' *  len(restaurant_cost_characters)
            # print(restaurant_cost)
        except:
            restaurant_cost = ""
        
        try:
            restaurant_location_section = chrome_driver1.find_element(By.CLASS_NAME, 'neighborhoodTag')
            restaurant_location = restaurant_location_section.text
            # print(restaurant_location)
        except:
            restaurant_location = ""
        
        try:
            review_text_section = chrome_driver1.find_element(By.CLASS_NAME, 'flatplan_body')
            review_text_pharagraphs = review_text_section.find_elements(By.CLASS_NAME, 'css-12lv66m')
            review_text = ""
            for review_text_pharagraph in review_text_pharagraphs:
                review_text += review_text_pharagraph.text + '\n'
            # print(review_text)
        except:
            review_text = ""
        
        try:
            review_date_section = chrome_driver1.find_element(By.TAG_NAME, 'time')
            review_date = review_date_section.get_attribute('datetime')
            # print(review_date)
        except:
            review_date = ""
        
        try:
            review_rating_section = chrome_driver1.find_element(By.CLASS_NAME, 'css-1hc0gxh')
            review_rating = review_rating_section.text
            # print(review_rating)
        except:
            review_rating = ""
        
        data.append([restaurant_name, restaurant_cuisine, restaurant_cost, restaurant_location, review_rating, review_text, review_date, review_url])
        chrome_driver1.quit()
    
    chrome_driver.quit()
    page_index += 1

# Scraping NY Times
restaurant_count = 0
chrome_driver = webdriver.Chrome(options=chrome_options)
chrome_driver.get(nytimes_url)
sleep(10)

try:
    modal_section = chrome_driver.find_element(By.CLASS_NAME, 'css-17og9h8')
    modal_continue_button = modal_section.find_element(By.TAG_NAME, 'button')
    modal_continue_button.click()
except:
    print("No Modal")

try:
    tracker_setting_section = chrome_driver.find_element(By.ID, 'dock-container')
    tracker_setting_close_button = tracker_setting_section.find_element(By.CLASS_NAME, 'css-brovj8')
    tracker_setting_close_button.click()
except:
    print("No tracker setting")

while True:
    try:
        restaurants_section = chrome_driver.find_element(By.CLASS_NAME, 'css-1wl2ztb')
        restaurants = restaurants_section.find_elements(By.CLASS_NAME, 'css-1hks1bt')
    except:
        # print("No restaurant section")
        break
    
    for restaurant in restaurants:
        restaurant_count += 1
        # print(restaurant_count)
        
        try:
            review_url = restaurant.find_element(By.TAG_NAME, 'a').get_attribute('href')
            # print(review_url)
        except:
            # print("No review url")
            break
        
        chrome_driver1 = webdriver.Chrome(options=chrome_options)
        chrome_driver1.get(archive_site + review_url)
        
        try:
            text_block = chrome_driver1.find_element(By.CLASS_NAME, 'TEXT-BLOCK')
            links = text_block.find_elements(By.TAG_NAME, 'a')
            archive_url = links[0].get_attribute('href')
        except:
            # print("archive error!")
            break
        
        chrome_driver2 = webdriver.Chrome(options=chrome_options)
        chrome_driver2.get(archive_url)
        
        try:
            review_date = chrome_driver2.find_element(By.TAG_NAME, 'time').get_attribute('datetime')[:10]
            # print(review_date)
        except:
            review_date = ""
            # print("No review date")
        
        try:
            restaurant_information_section = chrome_driver2.find_element(By.XPATH, "//div[@data-testid='restaurant-review-header']")
            restaurant_name = restaurant_information_section.find_element(By.TAG_NAME, 'dt').text
            # print(restaurant_name)
        except:
            restaurant_name = ""
            # print("No restaurant name")
        
        try:
            restaurant_informations = restaurant_information_section.find_elements(By.TAG_NAME, 'dd')
            review_rating = restaurant_informations[1].text[:-1] + " (" + restaurant_informations[0].text[:-1] + ")"
            # print(review_rating)
        except:
            review_rating = ""
            # print("No review rating")
        
        try:
            restaurant_cuisine = restaurant_informations[2].text[:-1]
            # print(restaurant_cuisine)
        except:
            restaurant_cuisine = ""
            # print("No restaurant cuisine")
        
        try:
            restaurant_cost = restaurant_informations[3].text[:-1]
            # print(restaurant_cost)
        except:
            restaurant_cost = ""
            # print("No restaurant cost")
        
        try:
            restaurant_location = restaurant_informations[4].text[:-1]
            # print(restaurant_location)
        except:
            restaurant_location = ""
            # print("No restaurant location")
        
        try:
            review_text_section = chrome_driver2.find_element(By.XPATH, "//section[@name='articleBody']")
            review_text = review_text_section.text
            review_text = review_text.replace("Image\n", "").replace("Credit...\n", "")
            # print(review_text)
        except:
            review_text = ""
            # print("No review text")
        
        chrome_driver2.quit()
        chrome_driver1.quit()
        data.append([restaurant_name, restaurant_cuisine, restaurant_cost, restaurant_location, review_rating, review_text, review_date, review_url])

    show_more_button_section = chrome_driver.find_element(By.CLASS_NAME, 'css-3qipg1')
    show_more_button = show_more_button_section.find_element(By.TAG_NAME, 'button')
    show_more_button.click()
    sleep(0.5)

# Scraping Michelin
page_index = 1
restaurant_count = 0

while True:
    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.get(michelin_url + str(page_index))
    restaurants_section = chrome_driver.find_element(By.CLASS_NAME, 'js-restaurant__list_items')
    restaurants = restaurants_section.find_elements(By.CLASS_NAME, 'col-md-6')

    if len(restaurants) == 0:
        break

    for restaurant in restaurants:
        restaurant_count += 1
        # print(restaurant_count)

        try:
            review_url_section = restaurant.find_element(By.CLASS_NAME, 'with-love')
            review_url = review_url_section.get_attribute('href')
            # print(review_url)
        except:
            # print("No Review URL")
            continue

        chrome_driver1 = webdriver.Chrome(options=chrome_options)
        chrome_driver1.get(review_url)
        sleep(5)

        try:
            restaurant_name_section = chrome_driver1.find_element(By.CLASS_NAME, 'restaurant-details__heading--title')
            restaurant_name = restaurant_name_section.text
            # print(restaurant_name)
        except:
            restaurant_name = ""
            # print("No Restaurant Name")

        try:
            restaurant_cuisine_price_section = chrome_driver1.find_element(By.CLASS_NAME, 'restaurant-details__heading-price')
            restaurant_cost = restaurant_cuisine_price_section.text.split(" · ")[0]
            restaurant_cuisine = restaurant_cuisine_price_section.text.split(" · ")[1]
            # print(restaurant_cuisine)
            # print(restaurant_cost)
        except:
            restaurant_cost = ""
            restaurant_cuisine = ""
            # print("No Restaurant Price")
            # print("No Restaurant Cuisine")

        try:
            restaurant_location_section = chrome_driver1.find_element(By.CLASS_NAME, 'restaurant-details__heading--address')
            restaurant_location = restaurant_location_section.text
            # print(restaurant_location)
        except:
            restaurant_location = ""
            # print("No Restaurant Location")

        try:
            review_rating_section = chrome_driver1.find_element(By.CLASS_NAME, 'restaurant-details__classification')
            review_rating = review_rating_section.text
            # print(review_rating)
        except:
            review_rating = ""
            # print("No Review Rating")

        try:
            review_text_section = chrome_driver1.find_element(By.CLASS_NAME, 'restaurant-details__description--text')
            review_text = review_text_section.text
            # print(review_text)
        except:
            review_text = ""
            # print("No Review Text")

        review_date = ""
        data.append([restaurant_name, restaurant_cuisine, restaurant_cost, restaurant_location, review_rating, review_text, review_date, review_url])
        chrome_driver1.quit()

    page_index += 1
    chrome_driver.quit()

# Specify the file path and name
file_path = 'out.csv'

# Open the file in write mode
with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)
    # Write the data to the CSV file
    writer.writerows(data)

# print('Data written to', file_path)