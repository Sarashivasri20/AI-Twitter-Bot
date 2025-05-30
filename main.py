import tweepy
import openai
import os
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup Twitter Client with all credentials
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    wait_on_rate_limit=True
)

# Function to generate AI reply
def generate_reply(user_tweet):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful, friendly AI replying to Twitter mentions in a warm and conversational tone."},
            {"role": "user", "content": user_tweet}
        ]
    )
    return response['choices'][0]['message']['content']

# Get your user ID
me = client.get_me()
user_id = me.data.id
print(f"✅ Authenticated as: @{me.data.username}")

# Get latest mentions
mentions = client.get_users_mentions(id=user_id)

# Check if there are any mentions
if mentions.data:
    print(f"🔁 Found {len(mentions.data)} mention(s). Responding to the latest one...")
    for tweet in mentions.data:
        user_text = tweet.text
        tweet_id = tweet.id
        author_id = tweet.author_id

        # Generate reply
        reply_text = generate_reply(user_text)
        print("📥 User:", user_text)
        print("🤖 Bot Reply:", reply_text)

        # Send the reply tweet (uncomment when ready to go live!)
        client.create_tweet(text=f"@{author_id} {reply_text}", in_reply_to_tweet_id=tweet_id)
        print("✅ (Reply ready to send — tweet sending is currently commented out)")
        break  # only respond to the latest mention
else:
    print("🕵️ No new mentions found. Try tweeting @yourusername and re-run this bot!")
