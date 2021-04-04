import asyncio
from telethon.sync import TelegramClient, events
from telethon.errors.rpcerrorlist import FloodWaitError
import requests
from datetime import datetime
from asyncio import Queue
import random
import logging
from asyncio_throttle import Throttler
import requests

from config import api_id, api_hash
destination_channel = 'https://t.me/joinchat/Hn89abajsihiM2Jl'
# k2_group_id = 554909334 # * test fd
k2_group_id = 1001387953586 # * k2 private ja vi
# k2_group_id = 1001465965123 # * k2 general ja vi
# vips = ["@dulx9666","https://t.me/dusub9666"]
vips = ["@MrZaos","@vanthucbk","@bibaoboi"]

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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";

async def alert_mess_worker(queue: Queue, throttler: Throttler, client: TelegramClient, des):
    while True:
        try:
            async with throttler:
                event =  await queue.get()
                await client.send_message(des, event.message)
                await asyncio.sleep(random.uniform(3.0,10.0 ))
        except FloodWaitError as e:
            logging.exception("flood wait error",exc_info=True)
            logging.warning('too much request')
            queue.put_nowait(event)
            await asyncio.sleep(500)
        except Exception as e:
            await client.send_message(des, 'ERROR!!!: ' + str(e))
            raise e

async def slack_alert_worker(queue: Queue, throttler:Throttler):
    while True:
        try:
            async with throttler:
                event =  await queue.get()
                sender = await event.get_sender()
                slack_data = {
                    'text': event.message.message,       
                    'blocks': [
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "*%s* - %s" % ( sender.username,event.message.message)
                            },
                        },
                ]}
                if event.message.media:
                    slack_data['blocks'].append({
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "has media"
                            },
                        })
                requests.post(SLACK_WEBHOOK_URL, json=slack_data)
        except Exception as e:
            logging.error(str(e), exc_info=True)
def run():
    async def _run():
        async with TelegramClient('name', api_id, api_hash) as client:
                queue = Queue()
                throttler = Throttler(rate_limit=5, period=10)
                # asyncio.create_task(alert_mess_worker(queue, throttler, client,des=destination_channel))
                asyncio.create_task(slack_alert_worker(queue, throttler))
                await client.send_message(destination_channel, 'INIT - %s - %s' % (k2_group_id, '+'.join(vips)))
                @client.on(events.NewMessage(chats=await client.get_entity(k2_group_id), from_users=vips))
                async def handler(event):
                    # sender = await event.get_sender()
                    print(event.message.message)
                    # event.message.message = sender.username + ': ' + event.message.message
                    queue.put_nowait(event)

                    # alert important
                    hour_tz = datetime.utcnow().hour + 9 
                    hour_tz = hour_tz - divmod(hour_tz,24)[0] * 24
                    if hour_tz >=0 and hour_tz <=9 and event.message.media:
                        requests.get("https://vybit.net/trigger/vpgobhuhwbg4hk7u")

                
                    
                await client.run_until_disconnected()
    asyncio.run(_run())