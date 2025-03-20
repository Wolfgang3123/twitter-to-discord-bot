import requests
import time
from bs4 import BeautifulSoup

# List of Twitter accounts to track (Nitter URLs)
NITTER_URLS = {
    "FutSheriff": "https://nitter.net/FutSheriff",
    "AsyFutTrader": "https://nitter.net/AsyFutTrader"
}

# Your Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1352212064990527529/hBMaYe_RyTpv7ANVx-clpVRqGc-MDZ3j6wgnXDyVjebFoV4eF4ddrKJo2Dv-OZFuaXsf"

# Store the last tweet for each account
last_tweets = {}

def get_latest_tweet(username, nitter_url):
    """Fetch the latest tweet from Nitter."""
    global last_tweets
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(nitter_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching tweets for {username}: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    tweet = soup.find("div", class_="tweet-content")  # Finds the latest tweet

    if tweet:
        tweet_text = tweet.get_text(strip=True)
        tweet_link = f"https://x.com/{username}"  # Link to actual tweet

        # Check if this tweet is new
        if username not in last_tweets or tweet_text != last_tweets[username]:
            last_tweets[username] = tweet_text  # Save latest tweet
            send_to_discord(username, tweet_text, tweet_link)

def send_to_discord(username, text, link):
    """Send tweet to Discord webhook."""
    message = f"🚨 **New Tweet from {username}:** {text} \n🔗 {link}"
    data = {"content": message}
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"Posted to Discord: {message}")
    except requests.RequestException as e:
        print(f"Error sending to Discord: {e}")

# Run the bot every 2 minutes
for username, nitter_url in NITTER_URLS.items():
    get_latest_tweet(username, nitter_url)
print("✅ Script executed successfully.")

