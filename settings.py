import os
from pathlib import Path  # Python 3.6+ only
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


API_TOKEN = os.getenv("API_TOKEN")
