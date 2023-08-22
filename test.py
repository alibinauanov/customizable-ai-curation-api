import openai
import apikey
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = apikey.api

def curate_content(input_data):
    curation_methods = input_data['curation_methods']
    content_to_curate = input_data['content_to_curate']

    # Process curation methods into a structured prompt
    curation_prompt = "\n".join([f"- {method}" for method in curation_methods])

    # Generate a single prompt for GPT-3.5 Turbo
    prompt = f"Given the following curation methods:\n{curation_prompt}\n\nCurate the following content:\n{content_to_curate}\n\nCurated Result:\n"

    # Call the OpenAI API to generate curated content using chat completion endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that curates content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )

    curated_result = response.choices[0].message['content'].strip()
    return curated_result

# Example input data
input_data = {
    "curation_methods": [
        "filter out tweets that are irrelevant to business",
        "summarize the rest into one paragraph",
        "each business related tweet should be summarized briefly into one sentence",
        "remove duplicated content"
    ],
    "content_to_curate": [
        "https://twitter.com/reachpathways",
        "https://twitter.com/connectcarehero",
        "https://twitter.com/mystrongcircle",
        "https://twitter.com/getroomii",
        "https://twitter.com/lisabmobility",
        "https://twitter.com/saferateco",
        "https://twitter.com/trust_clarity",
        "https://twitter.com/Kalima_KLX",
        "https://twitter.com/sanaraizen",
        "https://twitter.com/remoteshare",
        "https://twitter.com/officialedurain",
        "https://twitter.com/iteratehealth",
        "https://twitter.com/prosperetyinc",
        "https://twitter.com/MySmartCharts",
        "https://twitter.com/balodanafashion",
        "https://twitter.com/desksides",
        "https://twitter.com/use_tandem",
        "http://twitter.com/hellokadeya",
        "https://twitter.com/ShoppingSoftly",
        "https://twitter.com/Leagueswype",
        "https://twitter.com/ajmontgomery85",
        "https://twitter.com/SomneaHealth",
        "https://twitter.com/streoapp",
        "https://www.twitter.com/_kikrr_",
        "https://twitter.com/hublysurgical",
        "https://twitter.com/westxeast",
        "https://twitter.com/opnrmusic",
        "https://twitter.com/eventnoire",
        "https://twitter.com/graaphene",
        "https://twitter.com/kinkofahq",
        "https://twitter.com/hyivyhealth",
        "https://twitter.com/diiclae",
        "https://twitter.com/MinorityCircle",
        "https://twitter.com/demicomposting",
        "https://twitter.com/karma_trade",
        "https://twitter.com/BettorVision",
        "https://twitter.com/playlightpong",
        "https://twitter.com/ojaexpress",
        "https://twitter.com/BlipEnergy",
        "https://twitter.com/EBishaf"
    ]
}

def scrape_tweets_from_account(account_url):
    # Code to scrape tweets from the provided URL
    # Return the scraped tweet content as a list of strings
    response = requests.get(account_url)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find tweet elements (you need to inspect the page source to find the right selectors)
        tweet_elements = soup.select('.tweet-text')  # Adjust the selector
        
        # Extract tweet text from the elements
        tweets = [element.get_text() for element in tweet_elements]
        return tweets
    else:
        print(f"Failed to fetch tweets from {account_url}")
        return []

curated_content = []

# Modify the code to loop through each Twitter URL and scrape tweets
for account_url in input_data["content_to_curate"]:
    tweets = scrape_tweets_from_account(account_url)
    
    # Process the scraped tweets and add them to the curated content
    curated_content.append("\n".join(tweets))

# Join the curated content to form a single string
content_to_curate = "\n".join(curated_content)

# Call the curate_content function with the updated input
input_data["content_to_curate"] = content_to_curate
curated_output = curate_content(input_data)

# Print the curated result
print(curated_output)