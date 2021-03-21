from os import environ

from dotenv import load_dotenv
from discord.ext.utils import get_extensions

from bot import Bot


load_dotenv()

bot = Bot()

for extension in get_extensions("cogs"):
    bot.load_extension(extension)

bot.run(environ["TOKEN"])
