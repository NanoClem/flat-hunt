import re
from typing import Any
from w3lib.html import remove_tags

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


class ExtractSubStr:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def __call__(self, value: str) -> str | None:
        match = re.search(self.pattern, value)
        return match.group(0) if match else ""


class Replace:
    def __init__(self, to_replace: str, replace_val: str):
        self.to_replace = to_replace
        self.replace_val = replace_val

    def __call__(self, value: str) -> str:
        return value.replace(self.to_replace, self.replace_val)


def filter_empty(value: str) -> str | None:
    """Returns None if the string value is empty."""
    return value if value else None


def to_int(value: str | None) -> int | None:
    """Convert a string value to int if it is not empty or None. Otherwise returns None."""
    return int(value) if value else None


def ensure_min(value: int) -> int:
    """Ensures that the minimum value cannot go under 1."""
    return value if value >= 1 else 1


class FlatItem(scrapy.Item):

    source_id = scrapy.Field(
        input_processor=MapCompose(str),
        output_processor=TakeFirst(),
    )
    rent = scrapy.Field(
        input_processor=MapCompose(
            ExtractSubStr("[0-9]+'[0-9]+"), Replace("'", ''), to_int
        ),
        output_processor=TakeFirst(),
    )
    expenses = scrapy.Field(
        input_processor=MapCompose(
            ExtractSubStr("\+\s[0-9]+"), Replace('+ ', ''), to_int
        ),
        output_processor=TakeFirst(),
    )
    nb_bathrooms = scrapy.Field(
        input_processor=MapCompose(ensure_min),
        output_processor=TakeFirst(),
    )
    # ref = scrapy.Field(
    #     input_processor=MapCompose(remove_tags),
    #     output_processor=TakeFirst(),
    # )
    # floor = scrapy.Field(
    #     input_processor=MapCompose(remove_tags),
    #     output_processor=TakeFirst(),
    # )
    # availability = scrapy.Field(
    #     input_processor=MapCompose(remove_tags),
    #     output_processor=TakeFirst(),
    # )
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    lat = scrapy.Field(output_processor=TakeFirst())
    lon = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())
    # city = scrapy.Field(output_processor=TakeFirst())
    # postal_code = scrapy.Field(output_processor=TakeFirst())
    nb_rooms = scrapy.Field(output_processor=TakeFirst())
    nb_bedrooms = scrapy.Field(output_processor=TakeFirst())
    surface = scrapy.Field(output_processor=TakeFirst())
    nb_pics = scrapy.Field(output_processor=TakeFirst())
    pics = scrapy.Field()
