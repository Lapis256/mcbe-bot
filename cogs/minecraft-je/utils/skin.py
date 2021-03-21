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


async def get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return (response.status, await response.json())


async def fetch_uuid(name):
    url = BASE_URL + name
    status, response = await get_request(url)
    if status != 200:
        raise NotFoundUser

    return response["id"]


async def fetch_skin_url(uuid):
    url = SKIN_URL + uuid
    status, response = await get_request(url)
    if status != 200:
        raise NotFoundUser

    decoded = b64decode(response["properties"][0]["value"])
    decoded_json = json.loads(decoded)

    return decoded_json["textures"]["SKIN"]["url"]
