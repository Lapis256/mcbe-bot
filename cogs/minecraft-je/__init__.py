from discord.ext import commands
import discord

from .utils.skin import (
    fetch_uuid,
    fetch_skin_url,
    get_skin_url,
    get_render_url,
    NotFoundUser
)


class MinecraftJE(commands.Cog):
    @commands.command()
    async def getskin(self, ctx, name: str):
        """minecraft JEのスキンを取得します。"""
        uuid = await fetch_uuid(name)
        embed = discord.Embed(
            title=f"{name}'s skin",
            description=f"[Download]({get_skin_url(uuid)})"
        )
        embed.set_image(url=get_render_url(uuid))

        await ctx.send(embed=embed)

    @getskin.error
    async def getskin_error(self, ctx, error):
        original_error = getattr(error, 'original', error)

        if isinstance(original_error, NotFoundUser):
            await ctx.send("ユーザーが存在しません。")
            return

        raise error


def setup(bot):
    bot.add_cog(MinecraftJE(bot))
