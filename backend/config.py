from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="backend/login.env")  # Loads the environment variables from the .env file
print("Information Loaded")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

