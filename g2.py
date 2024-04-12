import requests
import csv
import time
import msvcrt

# API endpoint and API key
API_ENDPOINT = "https://data.g2.com/api/v1/products"
API_KEY = "376616154f49d1aff0a7a529dc66732eda1edcf0b1643e829722d1d9f0c939d2"

# Set the API key in the request headers
headers = {
    "Authorization": f"Token token={API_KEY}",
    "Content-Type": "application/vnd.api+json"
}

# Function to fetch products from the API
def fetch_products():
    url = API_ENDPOINT
    products = []
    product_count = 0

    # Open a CSV file for writing
    with open('g2.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header row
        csv_writer.writerow(["Product"])

        while url:
            # Send a GET request to the API endpoint
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Extract product names from the response
                for product_data in data.get("data", []):
                    name = product_data.get("attributes", {}).get("name")
                    if name:
                        csv_writer.writerow([name])  # Write the product name to the CSV file
                        products.append(name)
                        product_count += 1
                        print(f"Products fetched: {product_count}", end='\r')  # Print the product count

                        # Check if user wants to interrupt the extraction process
                        if msvcrt.kbhit():
                            key = msvcrt.getch().decode()
                            if key == '1':
                                print("\nExtraction interrupted by user.")
                                return products

                # Get the next page URL
                links = data.get("links", {})
                url = links.get("next")

                # Check if user wants to interrupt the extraction process
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode()
                    if key == '1':
                        print("\nExtraction interrupted by user.")
                        return products

            else:
                print(f"Error: {response.status_code} - {response.text}")
                break

            if response.headers.get('X-RateLimit-Limit') and int(response.headers['X-RateLimit-Limit']) <= 100:
                print("Rate limit close to being exceeded. Sleeping for 1 second to ensure compliance...")
                time.sleep(1)

    return products