from io import BytesIO

from nbtlib import File, CompoundSchema, parse_nbt
from .structure_schema import (
    ItemEntityStructureSchema,
    EntityStructureSchema,
    Entity
)


def _get_structure_object(entity):
    return {
        "format_version": 1,
        "size": [1, 1, 1],
        "structure_world_origin": [0, 0, 0],
        "structure": {
            "block_indices": [[-1], [-1]],
            "palette": {
                "default": {
                    "block_palette": [],
                    "block_position_data": {}
                }
            },
            "entities": [entity]
        }
    }


class EntityFileBase(File, CompoundSchema):
    def __init__(self, entity):
        super().__init__({
            "": _get_structure_object(entity.to_dict())
        }, gzipped=False, byteorder="little")

    @classmethod
    def create_file(cls, entity):
        buff = BytesIO()
        cls(entity).write(buff, byteorder="little")
        buff.seek(0)

        return buff

    @classmethod
    def create_file_with_tag(cls, entity, tag):
        self = cls(entity)
        self.add_tag(tag)
        buff = BytesIO()
        self.write(buff, byteorder="little")
        buff.seek(0)

        return buff

    def add_tag(self, tag):
        pass


class ItemEntityStructureFile(EntityFileBase):
    schema = {"": ItemEntityStructureSchema}

    @classmethod
    def create_file(cls, item):
        entity = Entity([0.5, 0.5, 0.5], "minecraft:item", item)
        return cls.create_file(entity)

    @classmethod
    def create_file_with_tag(cls, item, tag):
        entity = Entity([0.5, 0.5, 0.5], "minecraft:item", item)
        self = cls(entity)
        self.add_tag(tag)
        buff = BytesIO()
        self.write(buff, byteorder="little")
        buff.seek(0)

        return buff

    def add_tag(self, tag):
        self.root["structure"]["entities"][0]["Item"]["tag"] = parse_nbt(tag)


class EntityStructureFile(EntityFileBase):
    schema = {"": EntityStructureSchema}

    def add_tag(self, tag):
        self.root["structure"]["entities"][0].update(parse_nbt(tag))
