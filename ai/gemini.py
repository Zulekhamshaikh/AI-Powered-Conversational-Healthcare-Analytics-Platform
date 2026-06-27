import os
from dotenv import load_dotenv
from google import genai
from ai.prompt import SYSTEM_PROMPT

# Load .env file
load_dotenv()

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def ask_gemini(question, dashboard_summary):

    prompt = f"""
{SYSTEM_PROMPT}

Dashboard Summary

{dashboard_summary}

User Question

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"AI service is temporarily unavailable.\n\nDetails:\n{e}"