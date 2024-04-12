# G2
# Innovative Product Exploration Tool

Our solution is an innovative tool designed to explore various online platforms and uncover cutting-edge products. We focus on four primary sources, each providing unique insights into emerging technologies:

- **Tech News:** TechCrunch offers in-depth articles on startups and tech trends.
- **Marketplaces:** Product Hunt showcases trending products across diverse categories.
- **Startup Platforms:** BetaList and Pitchwall spotlight emerging startups and their innovations.
- **Social Media:** Reddit serves as a vibrant forum for discussions on technology and startups.

## Targeted Exploration
We explore specific sections on Product Hunt, including work productivity, finance, marketing & sales, platforms, web3, ecommerce, and AI, to uncover the latest innovations. Additionally, we target relevant subreddits on Reddit, such as entrepreneurship, startups, business, SaaS, and marketing, among others, to capture valuable discussions. From BetaList, we focus on business and B2B topics, and we explore the new products section in Pitchwall. Furthermore, we use TechCrunch's articles, focusing on business and B2B topics, to gain detailed insights.

## Tools Used
- **Beautiful Soup:** For parsing HTML and extracting relevant data from web pages.
- **Selenium:** For automating web browser interactions to navigate and extract data from dynamic websites.
- **Bard API:** Used for filtering B2B products, summarizing descriptions, and extracting essential information.
- **Schedule library:** For automating the extraction process and ensuring timely updates.

## How It Works
1. **Extraction from G2.com:** We start by extracting existing products from G2.com using the provided API. You can interrupt the extraction process at any time. Once complete, the tool will display the number of products extracted and save them to a CSV file.

2. **Main Menu Selection:** After extraction, a main menu will be displayed, offering you the option to choose from different sources of new products, including Betalist, TechCrunch, Reddit, Pitchwall, and Product Hunt.

3. **Extraction and Comparison:** Upon selecting a source, the tool will extract new products from that platform while comparing them with the products extracted from G2.com. It will then display the number of new products found and save them to a CSV file.

4. **Repeat Process:** You can repeat the process by returning to the main menu and selecting a different source. This allows for continuous exploration of new products across various platforms.

## Installation
Install the necessary dependencies by running:
```bash
pip install -r requirements.txt
playwright install
```
Run the main.py file:
```bash
python main.py
```
On some devices, you might need ot manually install ChromeDriver.
[ChromeDriver Installation Instructions]([https://sites.google.com/chromium.org/driver/](https://chromedriver.chromium.org/downloads))


## Note
For demonstration purposes, we have restricted ourselves to extracting only 30 products in some parts of the code. With just a few changes in code, we have the scaled up version as well
