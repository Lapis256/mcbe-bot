from io import StringIO
from typing import Union, Optional


from more_itertools import ichunked
from nbtlib import CastError
from discord.ext import commands
import discord

from .utils.structure import EntityStructureFile, ItemEntityStructureFile
from .utils.structure_schema import Item, Entity
from .utils.title import gen_title, is_valid_type
from .utils.flat import (
    get_block,
    create_level_data,
    create_mcworld
)


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

    @commands.command()
    async def flat(self, ctx, levelname, biome,
                   *blocks: commands.Greedy[Union[int, str]]):
        """カスタムされたフラットワールドを生成します。
        このコマンドによって生成されるワールドはBedrockEdition限定です。
        <blocks>は<ブロックID:データ値> <ブロック数>このように表記してください。
        また、データ値が0の場合は省略可能です。
        バイオームIDはwiki等を参照してください。
        https://minecraft.gamepedia.com/Biome#Biome_IDs
        サンプル
        .flat testflat-world plains bedrock:0 1 dirt 2 grass 1
        """

        if len(blocks) % 2 > 0:
            await ctx.send("ブロックの指定が間違っています。")
            return

        block_data = []
        for _block, count in ichunked(blocks, 2):
            block = get_block(_block)
            block_data.append({
                "block_name": block.id,
                "block_data": block.data,
                "count": count
            })

        level_data = create_level_data(block_data, biome, levelname)
        mcworld = create_mcworld(level_data)
        blocks_text = "\n".join(
            ["レイヤー{0}: ID: {1[block_name]}, データ値: {1[block_data]}, 個数: {1[count]}".format(i + 1, v)
             for i, v in enumerate(block_data)]
        )

        await ctx.send(
            f"ワールド名: {levelname}\nバイオーム: {biome}\n{blocks_text}",
            file=discord.File(mcworld, filename="FlatWorld.mcworld")
        )

    @commands.group(invoke_without_command=True)
    async def structure(self, ctx):
        """ストラクチャーファイルを生成するコマンドです。"""
        await ctx.send("サブコマンドを指定してください。")

    @structure.command()
    async def item(self, ctx, file_name, identifier, damage: int = 0, count: int = 1,
                   unbreakable: bool = False, name: Optional[str] = None,
                   lore: Optional[str] = None):

        """特殊なアイテムが保存されたストラクチャーを生成します。"""

        item_buff = ItemEntityStructureFile.create_file(Item.create_item(
            identifier, damage, count, unbreakable, name, lore
        ))

        await ctx.send(
            file=discord.File(item_buff, filename=file_name + ".mcstructure")
        )

    @structure.command()
    async def tagitem(self, ctx, file_name, identifier, damage: int = 0, count: int = 1,
                      *, tag: str = "{}"):

        """特殊なアイテムが保存されたストラクチャーを生成します。
        tag引数を使うことで複雑なアイテムを指定することができます。
        minecraftのNBTに関する知識が必要です。"""

        try:
            item_buff = ItemEntityStructureFile.create_file_with_tag(Item.create_item(
                identifier, damage, count), tag)
        except CastError as e:
            await ctx.send(f"tag変数が間違っています。\n```\n{e}```")
            return

        await ctx.send(
            file=discord.File(item_buff, filename=file_name + ".mcstructure")
        )

    @structure.command()
    async def entity(self, ctx, file_name, identifier, *, nbt: str = "{}") -> None:
        """エンティティを含むストラクチャーを生成します。
        nbt引数を使用する事でエンティティのnbtを変更することができます。
        """

        try:
            entity_buff = EntityStructureFile.create_file_with_tag(
                Entity([0.5, 0.0, 0.5], identifier), nbt
            )
        except CastError as e:
            await ctx.send(f"nbt変数が間違っています。\n```\n{e}```")
            return

        await ctx.send(
            file=discord.File(entity_buff, filename=file_name + ".mcstructure")
        )


def setup(bot):
    bot.add_cog(MinecraftBE(bot))
