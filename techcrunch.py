import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

# Set the API key directly in the script
os.environ['GOOGLE_API_KEY'] = 'AAIzaSyA2NML5oE2_TiF7gLY72pmsf0WcLZ0NRUE'

# Configure the SDK with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# URLs of the search pages
urls = [
    "https://search.techcrunch.com/search;_ylc=X3IDMgRncHJpZANZZ1dnaThqQlNlaWNiZ3VnYmtTNDBBBG5fc3VnZwMwBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMzBHF1ZXJ5A2IyYgR0X3N0bXADMTcxMjgyODgyNA--?p=b2b&fr=techcrunch",
    "https://search.techcrunch.com/search;_ylt=Awrg1bB8vxdmwMIFHLunBWVH;_ylc=X1MDMTE5NzgwMjkxOQRfcgMyBGZyA3RlY2hjcnVuY2gEZ3ByaWQDSkV4MFphWXpSVi5fRHBfSnhpVS53QQRuX3JzbHQDMARuX3N1Z2cDOARvcmlnaW4Dc2VhcmNoLnRlY2hjcnVuY2guY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAM4BHF1ZXJ5A2J1c2luZXNzBHRfc3RtcAMxNzEyODMyMzkz?p=business&fr2=sb-top&fr=techcrunch"
]

# Initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Check if new_product.csv exists, create it if not
if not os.path.exists("new_products.csv"):
    with open("new_products.csv", "w", newline='') as new_product_file:
        writer = csv.writer(new_product_file)
        writer.writerow(["Product Name", "Description"])

for url in urls:
    # Open URL in browser
    driver.get(url)
    
    # Initialize counter for tracking the number of products extracted
    product_count = 0
    
    try:
        # Find all elements with class "fz-20 lh-22 fw-b"
        elements = driver.find_elements(By.CLASS_NAME, "fz-20")
        
        for element in elements:
            if product_count >= 5: # Limit extraction to 30 products
                break
            
            href = element.get_attribute("href")
            
            # Open the URL of each product
            driver.get(href)
            
            try:
                # Find the <h1> element with class "article__title"
                h1_element = driver.find_element(By.CLASS_NAME, "article__title")
                title = h1_element.text
                
                # Find the <p> element with id "speakable-summary"
                p_element = driver.find_element(By.ID, "speakable-summary")
                summary = p_element.text
                
                # Combine title and summary for classification
                description = f"{title}\n{summary}"
                
                # Classify the product type using Gemini API
                prompt = f"Based on the following description, is this product likely a B2B or B2C offering?\n{description}"
                classification = model.generate_content(prompt)
                product_type = classification.text.strip().upper()
                
                # Use genai to potentially extract product name
                product_name_prompt = f"What is the product name or company or firm mentioned in the following description? Give None if there are no product/company/firm \n{description}"
                product_name_response = model.generate_content(product_name_prompt)
                potential_product_name = product_name_response.text.strip()

                description_prompt = f"Give me a one line desription of the product/firm/company in description. \n{description}"
                description_response = model.generate_content(description_prompt)
                description_name = description_response.text.strip()

                # Print the potential product name (optional)
                print("Potential Product Name:", potential_product_name)
                print("Description:", description_name)

                # Check if "b2b" is present in product_type and potential product name is not None
                if "b2b" in product_type.lower() and potential_product_name != "None":
                    # Append potential product name and description to new_products.csv
                    with open("new_products.csv", "a", newline='') as new_product_file:
                        writer = csv.writer(new_product_file)
                        writer.writerow([potential_product_name, description_name])
                    
                    # Increment the product count
                    product_count += 1
            except StaleElementReferenceException:
                print(f"Skipping URL: {href} - Stale element reference: stale element not found")
                continue
    except Exception as e:
        print(f"Skipping URL: {url} - {str(e)}")
        continue

# Close the browser
driver.quit()
