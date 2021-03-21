import json
from base64 import b64decode

import aiohttp


SKIN_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"
BASE_URL = "https://api.mojang.com/users/profiles/minecraft/"
CRAFTERS_BASE = "https://crafatar.com/"
RENDER_BASE = CRAFTERS_BASE + "renders/"
BODY_RENDER = RENDER_BASE + "body/"
SKINS = CRAFTERS_BASE + "skins/"


class NotFoundUser(Exception):
    pass


def get_skin_url(uuid):
    return SKINS + uuid


def get_render_url(uuid):
    return BODY_RENDER + uuid


async def fetch_uuid(name):
    url = BASE_URL + name
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise NotFoundUser
            return (await response.json())["id"]


async def fetch_skin_url(uuid):
    url = SKIN_URL + uuid
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise NotFoundUser
            response_json = await response.json()

    decoded = b64decode(response_json["properties"][0]["value"])
    decoded_json = json.loads(decoded)

    return decoded_json["textures"]["SKIN"]["url"]
