import json
from datetime import datetime

import scrapy

from . import utils
from .items import FlatItem


class JsonLoadingPipeline:
    """Load incoming item into a jsonlines file."""

    def open_spider(self, spider: scrapy.Spider) -> None:
        load_path = utils.get_src_path() / 'data' / spider.name
        load_path.mkdir(parents=True, exist_ok=True)
        filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonlines'
        self.file = open(load_path / filename, 'w', encoding='utf-8')

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.file.close()

    @utils.logged
    def process_item(self, item: FlatItem, spider: scrapy.Spider):
        line = json.dumps(item.to_dict(), ensure_ascii=False) + "\n"  # ensure utf-8 encoding
        self.file.write(line)
        return item
