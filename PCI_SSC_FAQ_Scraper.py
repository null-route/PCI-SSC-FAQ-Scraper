from bs4 import BeautifulSoup
import requests
import lxml
import json
import re

# This is a quick Python script that scrapes the PCI SSC's website for FAQ
# article numbers, creation dates, titles, and corresponding links.
# Their site doesn't include an index that allows you to view all the FAQ
# titles in one place (which can be helpful when quickly searching for
# information on a topic) so I built this.
# Inspired by github.com/robchahin's previous scraper.

# Define the main scraping/storing function
def scrape(num):

    # Define the link to scrape based on the integer passed as a parameter
    params = "?q=00000" + str(num)
    r = requests.get('https://pcissc.secure.force.com/faq/pkb2_Home' + params)

    # Select the Javasript element containing listOfLists and store it as a list
    soup = BeautifulSoup(r.text, 'lxml')
    pattern = re.compile('var listOfLists =')
    javascript = soup.find('script', string = pattern).text
    javalist = javascript.split('\n')

    # Remove leading+trailing brackets from the JSON collected
    raw_json = javalist[4].split('[[', 1)[-1]
    raw_json = raw_json[:-3]

    # Attempt to parse the JSON that was collected
    try:
        # Load the raw JSON that was collected
        parsed_json = json.loads(raw_json)

        # Print relevant fields to stdout for informational purposes
        print(parsed_json["articleNumber"])
        print(parsed_json['theAV']["Artticle_Create_Date_Original__c"])
        print(parsed_json["title"])

        # Write relevant information to the results CSV
        results.write(parsed_json["articleNumber"] + ","
        + parsed_json['theAV']["Artticle_Create_Date_Original__c"] + ",\""
        + parsed_json["title"] + "\","
        + "https://pcissc.secure.force.com/faq/articles/Frequently_Asked_Question/" + parsed_json['urlName']
        + "\n")

    # Throw an exception if there wasn't an FAQ listed under the given ID
    except ValueError:
        print("Decoding JSON has failed; there *probably* weren't any search results")

# Open the CSV for storing results and begin iterating through FAQ IDs
results = open('results.csv', 'w')
for num in range(1000, 1500):
    scrape(num)
results.close()
