import requests
import datetime
import os
import tweepy

# Load secrets from environment
AI_API_URL = "https://ai-agents-services-app-503377404374.us-east1.run.app/api/v1/ai-agents/generate_ai_response"
AI_USER_NAME = os.getenv("AI_USER_NAME", "Kumar")
AI_USER_EMAIL = os.getenv("AI_USER_EMAIL", "kumar@example.com")

# Twitter API credentials
TWITTER_API_KEY = os.getenv("KxonKyKbxBl1hBDEAisWGeiTS")
TWITTER_API_SECRET_KEY = os.getenv("8wrjDEZHeMJU8duOBu02Le5ujMbxfjmWhVX9ituMbaXE63rgmp")
TWITTER_ACCESS_TOKEN = os.getenv("1963029637623382017-QY5bSmLQIRuLeF0i17hX0tjhh0qkGb")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("oy4eiHTWnUStkyzzKPybhr6OQd8LK2rzLURVi0va0dwya")

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
        response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        content = response.json()
        print("✅ College Knowledge Drop generated:")
        print(content)

        # Post to Twitter/X
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)

        # For simplicity, post the first 280 chars (or split into multiple tweets if needed)
        text_to_post = str(content)[:280]
        api.update_status(status=text_to_post)
        print("✅ Posted to Twitter/X successfully!")

    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch newsletter:", e)
    except tweepy.TweepError as e:
        print("❌ Twitter posting failed:", e)

if __name__ == "__main__":
    generate_drop()
