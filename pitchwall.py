import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import google.generativeai as genai
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set the API key directly in the script
os.environ['GOOGLE_API_KEY'] = 'AIzaSyA2NML5oE2_TiF7gLY72pmsf0WcLZ0NRUE'

# Configure the SDK with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def classify_product_type(description):
    prompt = f"Based on the following description, is this product likely a B2B or B2C offering?\n{description}"
    classification = model.generate_content(prompt)
    return classification.text.strip().upper()

# Initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = 'https://pitchwall.co/new'
driver.get(url)

# Click the "I'll remember" button
try:
    remember_button = driver.find_element(By.CLASS_NAME, "button-lg")
    remember_button.click()
    time.sleep(1)
except:
    pass

# Wait for the product cards to load
time.sleep(3)

# Keep scrolling and clicking the "Show More..." button until 300 products are loaded
while len(driver.find_elements(By.CLASS_NAME, 'list-item')) < 30:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        load_more_button = driver.find_element(By.CLASS_NAME, "load-more")
        load_more_button.click()
        time.sleep(1)
    except:
        pass

# Extract product cards
soup = BeautifulSoup(driver.page_source, 'html.parser')
product_cards = soup.select('div.list-item.group')

# Check if products.csv and new_products.csv exist, create them if not
if not os.path.exists("products.csv"):
    with open("products.csv", "w", newline='', encoding='utf-8') as products_file:
        writer = csv.writer(products_file)
        writer.writerow(["Product Name", "Description"])

if not os.path.exists("new_products.csv"):
    with open("new_products.csv", "w", newline='', encoding='utf-8') as new_product_file:
        writer = csv.writer(new_product_file)
        writer.writerow(["Product Name", "Description"])

# Get existing product names from products.csv and new_products.csv
existing_names = set()
with open("products.csv", "r", newline='', encoding='utf-8') as products_file:
    products_reader = csv.reader(products_file)
    next(products_reader)  # Skip header row
    for row in products_reader:
        existing_names.add(row[0])

with open("new_products.csv", "r", newline='', encoding='utf-8') as new_product_file:
    new_products_reader = csv.reader(new_product_file)
    next(new_products_reader)  # Skip header row
    for row in new_products_reader:
        existing_names.add(row[0])

# Open new_products.csv in append mode
with open("new_products.csv", "a", newline='', encoding='utf-8') as new_product_file:
    writer = csv.DictWriter(new_product_file, fieldnames=["Product Name", "Description"])

    for card in product_cards:  # Process only the first 30 products
        # Extract product name
        
        name_element = card.find('h3').find('a')
        name = name_element.text.strip() if name_element else ''
        print("Name:", name)

        # Extract description
        description_element = card.find('p', class_='truncate')
        description = description_element.text.strip() if description_element else ''
        print("Description:", description)


        # Check if product type is B2B and name not in existing names
        try:
            product_type = classify_product_type(description)
            if "B2B" in product_type.upper() and name not in existing_names:
                # Write to new_products.csv
                writer.writerow({"Product Name": name, "Description": description})
        except Exception as e:
            print(f"Error processing product: {e}")

print("Filtered B2B products added to 'new_products.csv'")

# Close the browser
driver.quit()
