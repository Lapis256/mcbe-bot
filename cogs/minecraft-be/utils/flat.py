from collections import namedtuple
from io import BytesIO
import time
import json
import zipfile

from nbtlib import File, CompoundSchema, schema
from nbtlib.tag import (
    Int,
    Long,
    String,
    write_numeric,
    INT
)


Block = namedtuple("Block", ["id", "data"])

BedrockLevelData = schema("BedrockLevelData", {
    "FlatWorldLayers": String,
    "Generator": Int,
    "LastPlayed": Long,
    "LevelName": String,
    "StorageVersion": Int
})


class BedrockLevelFile(File, CompoundSchema):
    schema = {"": BedrockLevelData}

    def __init__(self, level_data, version=8):
        super().__init__({"": level_data}, gzipped=False, byteorder="little")
        self.version = version

    def write(self, buff, byteorder="little"):
        tmp = BytesIO()
        super().write(tmp, byteorder)
        tmp.seek(0)
        data = tmp.read()

        write_numeric(INT, self.version, buff, byteorder)
        write_numeric(INT, len(data), buff, byteorder)
        buff.write(data)


def get_block_data(block):
    splited = block.split(":")
    if splited[-1:][0].isdigit():
        return int(splited[-1:][0])
    return 0


def get_block(block):
    data = get_block_data(block)

    def predicate(id):
        return Block(id if ":" in id else "minecraft:" + id, data)

    if block.endswith(e := ":" + str(data)):
        return predicate(block[:-len(e)])

    return predicate(block)


def create_level_data(block_data, biome_id, levelname):
    layers = {
        "biome_id": biome_id,
        "block_layers": block_data,
        "encoding_version": 4
    }

    BedrockLevelFile({
        "FlatWorldLayers": json.dumps(layers, ensure_ascii=False),
        "Generator": 2,
        "LastPlayed": int(time.time()),
        "LevelName": levelname,
        "StorageVersion": 7
    }).write(level_data := BytesIO())

    return level_data.getvalue()


def create_mcworld(level_data):
    with zipfile.ZipFile(mcworld := BytesIO(), "w") as zf:
        zf.write("assets/world_icon.jpeg", arcname="world_icon.jpeg")
        zf.writestr("level.dat", level_data)
        zf.writestr("resource_packs/", "")
        zf.writestr("behavior_packs/", "")

    mcworld.seek(0)

    return mcworld
