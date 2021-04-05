import os
from dotenv import load_dotenv
load_dotenv()
api_id=os.environ.get('api_id')
api_hash=os.environ.get('api_hash')
slack_bot_token = os.environ.get('slack_bot_token')