from dotenv import load_dotenv
import os

load_dotenv()

SECRET = os.environ.get("SECRET")
DB_URL = os.environ.get("DB_URL")