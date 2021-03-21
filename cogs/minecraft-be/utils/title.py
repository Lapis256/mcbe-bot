from discord.ext import commands


def is_valid_type(type):
    if type not in ["title", "subtitle", "actionbar"]:
        raise commands.BadArgument


def gen_title(selector, type, content, score_name):
    result = f"title {selector} {type} "

    for i, v in enumerate(content):
        i += 1
        result += f"§@e[type=armor_stand, c=1, scores={{{score_name}={i}..}}]{v}"

    return result
