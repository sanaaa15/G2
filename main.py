import subprocess
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
g2_dir = os.getcwd()

def display_menu():
    print("\nMain Menu:")
    print("1. Betalist")
    print("2. Product Hunt")
    print("3. Pitchwall")
    print("4. TechCrunch")
    print("5. Reddit")
    print("0. Exit")

# Welcome message
print("Welcome to Product Discovery Tool!")

# Display the menu and handle user input
while True: 
    display_menu()
    choice = input("Enter your choice (0-5): ")
    
    if choice == '0':
        print("Exiting the program. Goodbye!")
        break

    elif choice == '1':
        print("Fetching products from Betalist...")
        betalist_path = os.path.join(g2_dir, "betalist.py")
        subprocess.run(['python', betalist_path])
    
    elif choice == '2':
        print("Fetching products from Product Hunt...")
        producthunt_path = os.path.join(g2_dir, "producthunt.py")
        subprocess.run(['python', producthunt_path])
        
    elif choice == '3':
        print("Fetching products from PitchWall...")
        pitchwall_path = os.path.join(g2_dir, "pitchwall.py")
        subprocess.run(["python", pitchwall_path])
    
    elif choice == '4':
        print("Fetching products from TechCrunch...")
        techcrunch_path = os.path.join(g2_dir, "techcrunch.py")
        subprocess.run(['python', techcrunch_path])
        
    elif choice == '5':
        print("Fetching products from Reddit...")
        reddit_path = os.path.join(g2_dir, "reddit.py")
        subprocess.run(['python', reddit_path])
        
    else:
        print("Invalid choice. Please enter a number between 0 and 5.")
