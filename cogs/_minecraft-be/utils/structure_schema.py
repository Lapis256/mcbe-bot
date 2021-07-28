from dataclasses import dataclass
from typing import Optional

from nbtlib import schema
from nbtlib.tag import (
    Int,
    Byte,
    Float,
    Short,
    List,
    String,
    Compound
)


@dataclass
class Ench:
    id: int
    lvl: int

    def to_dict(self):
        return self.__dict__


@dataclass
class ItemDisplay:
    Name: Optional[str] = None
    Lore: Optional[list[str]] = None

    def to_dict(self):
        result = {}
        for k, v in self.__dict__.items():
            if v is not None:
                result[k] = v
        return result


@dataclass
class ItemTag:
    display: Optional[ItemDisplay] = None
    Unbreakable: Optional[bool] = None

    def to_dict(self):
        result = {}
        for k, v in self.__dict__.items():
            if k == "Unbreakable":
                result[k] = int(v)
            elif k == "display":
                result[k] = v.to_dict()
        return result


@dataclass
class Item:
    Name: str
    Damage: int
    Count: int
    tag: ItemTag

    @classmethod
    def create_item(cls, id, damage=0, count=1, unbreakable=0, name=None, lore=None):
        if lore is not None:
            lore = [lore]
        return cls(
            id, damage, count,
            ItemTag(
                ItemDisplay(name, lore),
                unbreakable
            )
        )

    def to_dict(self):
        dict = self.__dict__
        dict["tag"] = self.tag.to_dict()
        return dict


@dataclass
class Entity:
    Pos: list[float]
    identifier: str
    Item: Optional[Item] = None

    def to_dict(self):
        dict = self.__dict__
        if dict["Item"] is None:
            del dict["Item"]
        else:
            dict["Item"] = self.Item.to_dict()

        return dict


EntitySchema = schema("EntitySchema", {
    "Pos": List[Float],
    "identifier": String,
})


ItemEntitySchema = schema("ItemEntitySchema", {
    **EntitySchema.schema,
    "Item": schema("Item", {
        "Name": String,
        "Damage": Short,
        "Count": Byte,
        "tag": schema("tag", {
            "display": schema("display", {
                "Name": String,
                "Lore": List[String]
            }),
            "ench": List[schema("ench", {
                "id": Short,
                "lvl": Short
            })],
            "Unbreakable": Byte
        })
    })
})


def _get_structure_schema(entity_schema):
    return {
        "format_version": Int,
        "size": List[Int],
        "structure_world_origin": List[Int],
        "structure": schema("structure", {
            "block_indices": List[List[Int]],
            "palette": schema("palette", {
                "default": schema("default", {
                    "block_palette": List[Int],
                    "block_position_data": Compound
                })
            }),
            "entities": List[entity_schema]
        })
    }


EntityStructureSchema = schema(
    "EntityStructureSchema", _get_structure_schema(EntitySchema))
ItemEntityStructureSchema = schema(
    "ItemEntityStructureSchema", _get_structure_schema(ItemEntitySchema))
