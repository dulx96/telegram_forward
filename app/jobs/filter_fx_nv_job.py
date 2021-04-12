import asyncio
from telethon.sync import TelegramClient, events
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.types import MessageMediaPhoto, MessageMediaWebPage
import requests
from datetime import datetime
from asyncio import Queue
import random
import logging
from asyncio_throttle import Throttler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os


from config import api_id, api_hash, slack_bot_token
destination_channel = 'https://t.me/joinchat/Hn89abajsihiM2Jl'
# k2_group_id = 554909334 # * test fd
k2_group_id = 1001387953586 # * k2 private ja vi
# k2_group_id = 1001465965123 # * k2 general ja vi
# vips = ["@dulx9666","https://t.me/dusub9666"]
vips = ["@MrZaos","@vanthucbk","@bibaoboi"]

slack_client = WebClient(token=slack_bot_token)

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
                if event.message.message:
                    blocks= [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": event.message.message
                            },
                        }]
                    slack_client.chat_postMessage(
                        channel="C01STR8P9ST",
                        text=(sender.username + ': ' + event.message.message),
                        blocks=blocks,
                        username=sender.username
                    )
                media = event.message.media
                if media:
                    if type(media) == MessageMediaPhoto:
                        try:
                            img_save_path = await event.download_media('images/')
                            slack_client.files_upload(
                                channels="C01STR8P9ST",
                                file=img_save_path,
                                initial_comment=sender.username
                                
                            )
                        except SlackApiError as e:
                            logging.error(str(e), exc_info=True)
                        finally:
                            os.remove(img_save_path)
        except Exception as e:
            slack_client.chat_postMessage(
                    channel="C01STR8P9ST",
                    text=('ERROR !!!\n' + str(e))
            )
            logging.error(str(e), exc_info=True)
def run():
    async def _run():
        async with TelegramClient('name', api_id, api_hash) as client:
                queue = Queue()
                throttler = Throttler(rate_limit=5, period=10)
                # asyncio.create_task(alert_mess_worker(queue, throttler, client,des=destination_channel))
                asyncio.create_task(slack_alert_worker(queue, throttler))
                await client.send_message(destination_channel, 'INIT - %s - %s' % (k2_group_id, '+'.join(vips)))
                @client.on(events.NewMessage(chats=k2_group_id, from_users=vips))
                async def handler(event):
                    queue.put_nowait(event)
                    # alert important
                    hour_tz = datetime.utcnow().hour + 9 
                    hour_tz = hour_tz - divmod(hour_tz,24)[0] * 24
                    if hour_tz >=0 and hour_tz <=9 and type(event.message.media) in [MessageMediaWebPage, MessageMediaPhoto]:
                        requests.get("https://vybit.net/trigger/vpgobhuhwbg4hk7u")
                await client.run_until_disconnected()
                # * alert if disconnected
                slack_client.chat_postMessage(
                        channel="C01STR8P9ST",
                        text=('DISCONNECTED !!!')
                )
    asyncio.run(_run())