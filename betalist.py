import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Use ChromeDriverManager to automatically install the appropriate chromedriver
service = Service(ChromeDriverManager().install())

# Function to scrape startup data from a given URL and write to CSV file
def scrape_and_write_startup_data(url):
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service)

    # Open the website
    driver.get(url)

    # Wait for 5 seconds for the page to load
    time.sleep(5)

    # Function to scroll down and wait for new elements to load
    def scroll_and_wait():
        # Scroll down
        driver.execute_script("window.scrollBy(0, 200);")
        # Wait for a brief moment to allow new elements to load
        time.sleep(2)

    # Initial scroll and wait
    scroll_and_wait()

    # Set to store existing products
    existing_products = set()

    # Check if CSV file exists and contains data
    csv_exists = os.path.exists("new_products.csv")
    if not csv_exists:
        with open("new_products.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Product Name", "Description"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    if csv_exists:
        with open("new_products.csv", "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_products.add(row["Product Name"])

    # Open CSV file in append mode
    with open("new_products.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product Name", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If CSV file is empty, write header row
        if not csv_exists:
            writer.writeheader()

        # Function to check if a product is already in existing products
        def is_new_product(product_name):
            return product_name not in existing_products

        # Initialize count for new products
        new_products_count = 0

        # Scroll and wait repeatedly until 30 new products are found or can't scroll anymore
        while new_products_count < 10:
            # Find all startup cards
            startup_cards = driver.find_elements(By.CLASS_NAME, "startupCard")

            # Iterate through each startup card
            for card in startup_cards:
                product_element = card.find_element(By.XPATH, ".//a[@class='block whitespace-nowrap text-ellipsis overflow-hidden font-medium']")
                product_name = product_element.text
                if is_new_product(product_name):
                    # Extract description
                    description_element = card.find_element(By.XPATH, ".//a[@class='block text-gray-500 dark:text-gray-400']")
                    description = description_element.text

                    # Write to CSV
                    writer.writerow({"Product Name": product_name, "Description": description})

                    # Add to existing products set
                    existing_products.add(product_name)

                    # Increment count for new products
                    new_products_count += 1

            # Scroll down again
            scroll_and_wait()

    # Close the WebDriver
    driver.quit()

# List of URLs to scrape
urls = [
    "https://betalist.com/topics/b2b",
    "https://betalist.com/topics/business-services"
]

# Scrape data for each URL and write to new_products.csv
for url in urls:
    scrape_and_write_startup_data(url)

print("Data has been written to new_products.csv")
