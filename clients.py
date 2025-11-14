# client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise RuntimeError("Set PERPLEXITY_API_KEY in your environment or .env file")

# Use the OpenAI-compatible client but point base_url to Perplexity pplx endpoint
client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")