from api.modules.notion import notion
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(f'{Path(__file__).resolve().parent}/.env')
api_key = os.getenv('notion_key')

authNotion = notion(api_key)
print(authNotion.get_dbs())
