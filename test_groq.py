import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {'✅ YES' if api_key else '❌ NO'}")
print(f"Key starts with: {api_key[:10]}..." if api_key else "No key found")

from groq import Groq
client = Groq(api_key=api_key)
print("✅ Groq client initialized successfully!")