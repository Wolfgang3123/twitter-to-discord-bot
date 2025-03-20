ECHO is on.

import requests
import time
from bs4 import BeautifulSoup

# List of Twitter accounts to track
TWITTER_ACCOUNTS = [
    "https://x.com/AsyFutTrader",  # Account 1
    "https://x.com/EASPORTSFC",    # Account 2
    "https://x.com/FutSheriff"     # Account 3
]

# Your Discord Webhook URL (replace with your actual webhook)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1352212064990527529/hBMaYe_RyTpv7ANVx-clpVRqGc-MDZ3j6wgnXDyVjebFoV4eF4ddrKJo2Dv-OZFuaXsf"

# Store the last tweet for each account to avoid duplicates
last_tweets = {}

def get_latest_tweet(account_url):
    """Fetch the latest tweet from a Twitter profile page."""
    global last_tweets
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(account_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find tweets in the page source
    tweets = soup.find_all("article")
    if tweets:
        tweet_text = tweets[0].get_text(strip=True)
        tweet_link = account_url  # Twitter blocks direct tweet links

        if account_url not in last_tweets or tweet_text != last_tweets[account_url]:
            last_tweets[account_url] = tweet_text  # Save latest tweet
            send_to_discord(account_url, tweet_text, tweet_link)

def send_to_discord(account, text, link):
    """Send tweet to Discord webhook."""
    message = f"🚨 **New Tweet from {account}:** {text} \n🔗 {link}"
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    print(f"Posted to Discord: {message}")

# Run the bot every 2 minutes
while True:
    for account in TWITTER_ACCOUNTS:
        get_latest_tweet(account)
    time.sleep(120)  # Wait 2 minutes before checking again
