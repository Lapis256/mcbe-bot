from discord.ext import commands
from uvloop import new_event_loop


async def _get_prefix(bot, message):
    prefix = (".", )
    return commands.when_mentioned_or(*prefix)(bot, message)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=_get_prefix,
            case_insensitive=True,
            loop=new_event_loop(),
            *args, **kwargs
        )
