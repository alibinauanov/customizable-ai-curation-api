import openai
import requests
import apikey
from bs4 import BeautifulSoup

# Set your OpenAI API key directly
openai.api_key = apikey.api

def curate_content(input_data):
    curation_methods = input_data['curation_methods']
    content_to_curate = input_data['content_to_curate']

    # Process curation methods into a structured prompt
    curation_prompt = "\n".join([f"- {method}" for method in curation_methods])

    # Generate a single prompt for GPT-3.5 Turbo
    prompt = f"Given the following curation methods:\n{curation_prompt}\n\nCurate the following content:\n{content_to_curate}\n\n Write the names of accounts from content_to_curate. Curated Result:\n"

    # Call the OpenAI API to generate curated content using chat completion endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": "You are a helpful assistant that curates content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )

    curated_result = response.choices[0].message['content'].strip()
    return curated_result

def scrape_tweets_from_account(account_url):
    response = requests.get(account_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tweet_elements = soup.select('.tweet-text')  # Adjust the selector
        
        tweets = [element.get_text() for element in tweet_elements]
        return tweets
    else:
        print(f"Failed to fetch tweets from {account_url}")
        return []

def get_account_name(account_url):
    # Extract the account name from the URL (you may need to customize this logic)
    account_name = account_url.split('/')[-1]
    return account_name

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

curated_content = []

for account_url in input_data["content_to_curate"]:
    account_name = get_account_name(account_url)
    tweets = scrape_tweets_from_account(account_url)
    
    # Process the scraped tweets and add them to the curated content
    curated_tweets = []

    for tweet in tweets:
        # Apply your specific curation methods here
        # For demonstration, we'll add a simple prefix
        curated_tweet = f"- Summarized tweet from {account_name}: {tweet}"  
        curated_tweets.append(curated_tweet)

    # Include account name and curated tweets in the content
    curated_content.extend(curated_tweets)

content_to_curate = "\n\n".join(curated_content)
input_data["content_to_curate"] = content_to_curate

curated_output = curate_content(input_data)
print("Based on the given curation methods, the content has been curated as follows:")
print(curated_output)
