import asyncio
from telethon.sync import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto
from asyncio import Queue
import logging
from asyncio_throttle import Throttler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os


from config import api_id, api_hash, slack_bot_token

group_id = 1001512735887 # * k2 private 

vips = ["@HeaLerREAL"]

channel = "C02BNS88JGY"

slack_client = WebClient(token=slack_bot_token)


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
                        channel=channel,
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
                                channels=channel,
                                file=img_save_path,
                                initial_comment=sender.username
                                
                            )
                        except SlackApiError as e:
                            logging.error(str(e), exc_info=True)
                        finally:
                            os.remove(img_save_path)
        except Exception as e:
            slack_client.chat_postMessage(
                    channel=channel,
                    text=('ERROR !!!\n' + str(e))
            )
            logging.error(str(e), exc_info=True)
def run():
    async def _run():
        async with TelegramClient('name', api_id, api_hash) as client:
                queue = Queue()
                throttler = Throttler(rate_limit=5, period=10)
                asyncio.create_task(slack_alert_worker(queue, throttler))
                @client.on(events.NewMessage(chats=group_id, from_users=vips))
                async def handler(event):
                    queue.put_nowait(event)
                await client.run_until_disconnected()
                # * alert if disconnected
                slack_client.chat_postMessage(
                        channel=channel,
                        text=('DISCONNECTED !!!')
                )
    asyncio.run(_run())