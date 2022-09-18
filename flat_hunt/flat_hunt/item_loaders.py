import re
from w3lib.html import remove_tags

from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity


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


class FlatLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    source_id_in = MapCompose(str)
    rent_in = MapCompose(ExtractSubStr("[0-9]+'[0-9]+"), Replace("'", ''), to_int)
    expenses_in = MapCompose(ExtractSubStr("\+\s[0-9]+"), Replace('+ ', ''), to_int)
    nb_bathrooms_in = MapCompose(ensure_min)
    ref_in = MapCompose(remove_tags)
    floor_in = MapCompose(remove_tags)
    availability_in = MapCompose(remove_tags)
