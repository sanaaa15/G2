import csv
import os
import praw
import google.generativeai as genai
from prawcore.exceptions import NotFound

# Set the API key directly in the script
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCCemIFkG96pJ1wqKVScS0ygADpngsrBJc'
# Configure the SDK with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Replace these with your own credentials
client_id = 'LNM59gQzm5PbZSXG934Y4Q'
client_secret = 'AMuxl3xvyTUWG8LzYK3Jh9J2_fTq2w'
user_agent = 'MyRedditScraper/0.1 by u/CourageMotor8658'

# Initialize the Reddit instance
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# List of subreddits you want to scrape
subreddits = [        "entrepreneur",  # General entrepreneurship, many B2B discussions
    "startups",  # Startups in general, often B2B focused
    "business",  # General business discussions, can unearth B2B companies
    "SaaS",  # Software as a Service, a major B2B category
    "marketing",  # Marketing discussions, often B2B focused
    "sales",  # Sales discussions and strategies, often B2B relevant
    "cloudcomputing",  # Cloud computing solutions, a large B2B market
    "cybersecurity",  # Cybersecurity solutions, a growing B2B market
    "fintech",  # Financial technology, a major B2B industry
    "supplychain",  # Supply chain management solutions, B2B focused
    "logistics",  # Logistics solutions, relevant to B2B businesses
    "artificial",  # Artificial intelligence discussions, with B2B applications
    "machinelearning",  # Machine learning discussions, with B2B applications
    "bigdata",  # Big data discussions and solutions, B2B focused

    "entrep",  # Short for entrepreneur, similar to r/entrepreneur
    "business_ideas",  # Discussions on new business ideas, including B2B
    "smallbusiness",  # Discussions relevant to small businesses, some B2B
    "contentmarketing",  # Content marketing strategies, B2B applications
    "socialmedia",  # Social media marketing discussions, B2B applications
    "SEO",  # Search engine optimization, B2B marketing strategy
    "webdev",  # Web development discussions, can unearth B2B service providers
    "appdevelopment",  # App development discussions, B2B service providers
    "marketingautomation",  # Marketing automation tools, B2B technology
    "crm",  # Customer relationship management, B2B software

    # Niche B2B areas
    "salesops",  # Sales operations discussions and tools
    "marketingops",  # Marketing operations discussions and tools
    "procurement",  # Procurement discussions and solutions
    
    "projectmanagement",  # Project management tools and strategies (B2B relevant)
    "datavisualization",  # Data visualization tools (B2B relevant)
    "businessintelligence",  # Business intelligence tools (B2B relevant)
    "b2bmarketing",  # B2B marketing specific discussions



]

# Function to check if the product is likely a B2B offering
def is_b2b(description):
    prompt = f"Based on the following description, is this product likely a B2B or B2C offering?\n{description}"
    classification = model.generate_content(prompt)
    return "B2B" in classification.text.strip().upper()

def fetch_and_process_posts(subreddit_names):
    new_products_set = set()  # Set to store unique product names already written
    # Check if new_products.csv exists, create it if not
    if not os.path.exists("new_products.csv"):
        with open("new_products.csv", "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Product Name", "Description"])
    # Load existing product names into the set
    with open("new_products.csv", "r", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            new_products_set.add(row[0])
    with open("new_products.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for subreddit_name in subreddit_names:
            try:
                subreddit = reddit.subreddit(subreddit_name)
            except NotFound as e:
                print(f"Error: Subreddit '{subreddit_name}' not found. Skipping...")
                continue
            print(f"Processing posts in /r/{subreddit_name}:")
            for submission in subreddit.hot(limit=5):  # You can change 'hot' to 'new' for latest posts
                if submission.selftext:
                    # Use genai to generate description
                    description_prompt = f"Give me a one line description of the following post: \n{submission.title}\n{submission.selftext}"
                    description_response = model.generate_content(description_prompt)
                    if description_response.parts and description_response.parts[0].text:
                        description = description_response.parts[0].text.strip()
                    else:
                        print(f"Error: Description could not be generated for post {submission.title}")
                        continue
                else:
                    description = "No description available."
                # Use genai to potentially extract product name
                product_name_prompt = f"What is the product name or company or firm mentioned in the following description? Give None if there are no product/company/firm \n{description}"
                product_name_response = model.generate_content(product_name_prompt)
                if product_name_response.parts and product_name_response.parts[0].text:
                    potential_product_name = product_name_response.parts[0].text.strip()
                else:
                    print(f"Error: Product name could not be extracted for description {description}")
                    continue

                # Check if potential product name is not None, if the product is likely a B2B offering, and if it's not already in new_products_set
                if potential_product_name != "None" and is_b2b(description) and potential_product_name not in new_products_set:
                    # Write the product name and description to CSV file
                    writer.writerow([potential_product_name, description])
                    print(f"Potential Product Name: {potential_product_name}")
                    print(f"Description: {description}")
                    print("---")
                    # Add the product name to new_products_set
                    new_products_set.add(potential_product_name)

# Call the function with your list of subreddits
fetch_and_process_posts(subreddits)



