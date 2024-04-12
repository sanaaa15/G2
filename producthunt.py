import os
import csv
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright
import google.generativeai as genai

# Set the API key directly in the script
os.environ['GOOGLE_API_KEY'] = 'AIzaSyA2NML5oE2_TiF7gLY72pmsf0WcLZ0NRUE'

# Configure the SDK with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def classify_product_type(description):
    prompt = f"Based on the following description, is this product likely a B2B or B2C offering?\n{description}"
    classification = model.generate_content(prompt)
    return classification.text.strip().upper()

async def extract_products_from_url(url):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)

        for n in range(0, 2):  # Scroll down multiple times to load more products
            show_more = await page.query_selector('text=Show more')
            await show_more.click()
            await asyncio.sleep(1)

        soup = BeautifulSoup(await page.content(), 'html.parser')
        products = []
        product_cards = soup.select('.flex.flex-col.pb-12 > div.mb-10')

        # Extract only 10 products from each category
        for index, card in enumerate(product_cards):
            if index >= 10:
                break

            # Extract title and link
            title_element = card.select_one('div.flex.flex-row.items-center > a > div.text-18.font-semibold.text-blue')
            title = title_element.text.strip() if title_element else ''

            # Extract description using the new selector
            description_element = card.select_one('div.text-14.sm\\:text-16.font-normal.text-light-grey.mb-6')
            description = description_element.text.strip() if description_element else ''

            # Classify product type using Gemini API
            product_type = classify_product_type(description)

            # Append product data to list if it's B2B
            if 'B2B' in product_type:
                products.append({
                    'Product Name': title,
                    'Description': description,
                })

        await browser.close()
        return products

async def main():
    # List of URLs to extract products from
    urls = [
        'https://www.producthunt.com/categories/work-productivity',
        'https://www.producthunt.com/categories/finance',
        'https://www.producthunt.com/categories/marketing-sales',
        'https://www.producthunt.com/categories/platforms',
        'https://www.producthunt.com/categories/web3',
        'https://www.producthunt.com/categories/ecommerce',
        'https://www.producthunt.com/categories/ai'
    ]

    # Extract products from each URL and save them to new_products.csv
    all_products = []
    for url in urls:
        products = await extract_products_from_url(url)
        all_products.extend(products)

    # Check if new_products.csv exists, create it if not
    if not os.path.exists("new_products.csv"):
        with open("new_products.csv", "w", newline='', encoding='utf-8') as new_product_file:
            writer = csv.writer(new_product_file)
            writer.writerow(["Product Name", "Description"])

    # Check if product already exists in products.csv
    existing_product_names = set()
    if os.path.exists("products.csv"):
        with open("products.csv", "r", newline='', encoding='utf-8') as products_file:
            products_reader = csv.reader(products_file)
            next(products_reader)  # Skip header row
            for row in products_reader:
                existing_product_names.add(row[0])

    # Open new_products.csv in append mode
    with open("new_products.csv", "a", newline='', encoding='utf-8') as new_product_file:
        writer = csv.DictWriter(new_product_file, fieldnames=["Product Name", "Description"])

        # Iterate over products and write them to new_products.csv if they don't already exist in products.csv
        for product in all_products:
            product_name = product["Product Name"]
            description = product["Description"]
            
            if product_name not in existing_product_names:
                # Write product to new_products.csv
                writer.writerow({"Product Name": product_name, "Description": description})

    print("Products filtered and saved to 'new_products.csv'")

# Run the async main function
asyncio.run(main())
