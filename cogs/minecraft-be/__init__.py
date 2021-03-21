from io import StringIO

from discord.ext import commands
import discord

from .utils.title import gen_title, is_valid_type


class MinecraftBE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def title(self, ctx, selector, title_type, content, score_name):
        """徐々に表示されるTitleコマンドを生成します。"""
        is_valid_type(title_type)

        title = gen_title(selector, title_type, content, score_name)

        if 2000 > len(title):
            await ctx.send(title)
        else:
            await ctx.send(
                "文字制限を超えたためファイルにまとめられました。",
                file=discord.File(StringIO(title), filename="title.txt")
            )

    @title.error
    async def title_error(self, ctx, error):
        original_error = getattr(error, 'original', error)

        if isinstance(original_error, commands.BadArgument):
            await ctx.send("タイトルのタイプが間違っています。")
            return

        raise error


def setup(bot):
    bot.add_cog(MinecraftBE(bot))
