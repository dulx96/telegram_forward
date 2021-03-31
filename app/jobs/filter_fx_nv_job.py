from telethon.sync import TelegramClient, events
import requests
from datetime import datetime
from config import api_id, api_hash
destination_channel = 'https://t.me/joinchat/Hn89abajsihiM2Jl'
# k2_group_id_test = 554909334
k2_group_id = 1001387953586
# vips = ["@dulx9666"]
vips = ["@Trangmin0335774138","@MrZaos","@vanthucbk","@bibaoboi"]
def run():
    with TelegramClient('name', api_id, api_hash) as client:
        @client.on(events.NewMessage(chats=client.get_entity(k2_group_id), from_users=vips))
        async def handler(event):
            sender = await event.get_sender()
            event.message.message = sender.username + ': ' + event.message.message  
            await client.send_message(destination_channel,event.message)
            hour_tz = datetime.utcnow().hour + 9 
            hour_tz = hour_tz - divmod(hour_tz,24)[0] * 24
            print(hour_tz)
            if hour_tz >=0 and hour_tz <=9 and event.message.media:
                requests.get("https://vybit.net/trigger/vpgobhuhwbg4hk7u")
            
        client.run_until_disconnected()