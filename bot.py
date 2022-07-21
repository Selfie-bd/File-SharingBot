#(©)Codexbotz

import pyromod.listen
from pyrogram import Client
import sys

from config import API_HASH, APP_ID, API_KEY, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/umlinks for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/umlinks for support")
            sys.exit()

        self.set_parse_mode("html")
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by 𝘾𝙤𝙙𝙚 𝕏 𝘽𝙤𝙩𝙯\nhttps://t.me/umlinks")
        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

async def get_shortlink(links, x):
    url = f'https://shorte.st/api'
    params = {'api': API_KEY,
              'url': links,
              'alias': x
              }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            print(data["status"])
            if data["status"] == "success":
                return f"<code>{data['shortenedUrl']}</code>\n\nHere is your Link:\n{data['shortenedUrl']}"
            else:
                return f"Error: {data['message']}"


async def replace_link(text, x):
    text = await replace_username(text)
    links = re.findall(r'https?://[^\s]+', text)
    for link in links:

        if INCLUDE_DOMAIN:
            include = INCLUDE_DOMAIN.split(',')
            domain = [domain.strip() for domain in include]
            if any(i in link for i in domain):
                short_link = await get_shortlink(link, x)
                text = text.replace(link, short_link)


        elif EXCLUDE_DOMAIN:
            exclude = EXCLUDE_DOMAIN.split(',')
            domain = [domain.strip() for domain in exclude]
            if any(i in link for i in domain):
                pass
            else:
                short_link = await get_shortlink(link, x)

                text = text.replace(link, short_link)

        else:
            short_link = await get_shortlink(link, x)

            text = text.replace(link, short_link)

    return text

bot.run()
