from config import api_id, api_hash
from telethon.sync import TelegramClient

def run(dialog_name:str):
   with TelegramClient('name', api_id=api_id, api_hash=api_hash) as client:
      my_private_channel = None
      my_private_channel_id = None
      for dialog in client.iter_dialogs():
         if dialog.name == dialog_name:
            my_private_channel = dialog
            my_private_channel_id = dialog.id
            break

      if my_private_channel is None:
         print("chat not found")
      else:
         print("chat id is", my_private_channel_id)