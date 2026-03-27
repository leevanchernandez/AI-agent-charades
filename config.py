import os
from dotenv import load_dotenv

# This command looks for the .env file and loads the secrets inside it
load_dotenv() 

# Now we can grab the key securely!
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: Gemini API Key not found. Check your .env file!")
    
VISION_MODEL = "gemini-3-flash"