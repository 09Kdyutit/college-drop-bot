import requests
import datetime
import os
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

# AI Agent
AI_API_URL = "https://ai-agents-services-app-503377404374.us-east1.run.app/api/v1/ai-agents/generate_ai_response"
AI_USER_NAME = os.getenv("AI_USER_NAME", "Kumar")
AI_USER_EMAIL = os.getenv("AI_USER_EMAIL", "kumar@example.com")

# Twitter API v2
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def generate_drop():
    today = datetime.date.today().strftime("%B %d, %Y")
    subject = "Biology"

    prompt = f"""
You are an expert college admissions coach. Produce one "College Knowledge Drop" newsletter for {today}.
Structure exactly as:
1) Admissions Tip of the Day — one practical high-impact tip with 2-3 bullet action steps and a short example of a student who used it.
2) Scholarship/Opportunity Spotlight — choose one active opportunity (scholarship, program, or internship). Give name, 1-line description, eligibility, deadline (exact date if known or state 'TBD'), application link, and 2-sentence pitch why it matters.
3) Academic Mini-Lesson — 150-200 words on a college-level concept. The subject for today is {subject}. Write simply, include one short example or analogy and a 1-question practice prompt.
4) Essay Inspiration Prompt — a unique prompt and 3 reflection questions.
5) Mindset & Motivation Quote — include quote and one-sentence application.

Return output with clear headings, emojis, and short bullet lists. Keep it concise, suitable for conversion into a Twitter thread.
"""

    payload = {
        "prompt": prompt,
        "user_name": AI_USER_NAME,
        "user_email": AI_USER_EMAIL
    }

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    try:
        # Generate newsletter
        response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        content = response.json()
        newsletter_text = content.get("response", "")
        print("✅ College Knowledge Drop generated:\n")
        print(newsletter_text[:500] + "...\n")  # first 500 chars for preview

        # Post to Twitter/X v2
        client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

        # Twitter v2 can only post one tweet at a time
        tweet_text = newsletter_text[:280]  # simple approach for first tweet
        client.create_tweet(text=tweet_text)
        print("✅ Posted to Twitter/X successfully!")

    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch newsletter:", e)
    except tweepy.TweepyException as e:
        print("❌ Twitter posting failed:", e)

if __name__ == "__main__":
    generate_drop()
