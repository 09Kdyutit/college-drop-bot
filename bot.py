import requests
import datetime
import os

# AI Agents API endpoint
AI_API_URL = "https://ai-agents-services-app-503377404374.us-east1.run.app/api/v1/ai-agents/generate_ai_response"

# Environment variables for user info
AI_USER_NAME = os.getenv("AI_USER_NAME", "Kumar")
AI_USER_EMAIL = os.getenv("AI_USER_EMAIL", "kumar@example.com")

def generate_drop():
    today = datetime.date.today().strftime("%B %d, %Y")
    subject = "Biology"  # You can rotate subjects manually or add rotation logic

    prompt = f"""
You are an expert college admissions coach. Produce one "College Knowledge Drop" newsletter for {today}.
Structure exactly as:
1) Admissions Tip of the Day — one practical high-impact tip with 2-3 bullet action steps and a short example of a student who used it.
2) Scholarship/Opportunity Spotlight — choose one active opportunity (scholarship, program, or internship). Give name, 1-line description, eligibility, deadline (exact date if known or state 'TBD'), application link, and 2-sentence pitch why it matters.
3) Academic Mini-Lesson — 150-200 words on a college-level concept. The subject for today is {subject}. Write simply, include one short example or analogy and a 1-question practice prompt.
4) Essay Inspiration Prompt — a unique prompt and 3 reflection questions.
5) Mindset & Motivation Quote — include quote and one-sentence application.

Return output with clear headings, emojis, and short bullet lists. Keep it concise, suitable for conversion into a Twitter thread, Instagram carousel slides, and a short TikTok script.
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
        print("✅ College Knowledge Drop:")
        print(content)
    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch newsletter:", e)

if __name__ == "__main__":
    generate_drop()
