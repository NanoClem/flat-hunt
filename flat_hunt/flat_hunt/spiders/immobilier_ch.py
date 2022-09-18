import re
import json
from typing import Callable

import scrapy
from scrapy.loader import ItemLoader

from flat_hunt.items import FlatItem


class ImmobilierChSpider(scrapy.Spider):
    name = 'immobilier_ch'
    allowed_domains = ['www.immobilier.ch']
    start_urls = ['https://www.immobilier.ch/umbraco/Surface/Estate/GetMapItems']

    headers: dict = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    json_headers: dict = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    cookies: dict = {
        'ASP.NET_SessionId': 'pcerzkiru3jsgkusj1vglnea',
    }

    def make_request(
        self, url: str, headers: dict, callback: Callable, cb_kwargs: dict | None = None
    ):
        return scrapy.Request(
            url=url,
            headers=headers,
            cookies=self.cookies,
            callback=callback,
            cb_kwargs=cb_kwargs or {},
        )

    def start_requests(self):
        yield self.make_request(
            url=self.start_urls[0],
            headers=self.json_headers,
            callback=self.parse,
        )

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        flats_data = data['Results']

        for item in flats_data:
            req = self.make_request(
                url=f'https://{self.allowed_domains[0]}/{item["u"]}',
                headers=self.headers,
                callback=self.parse_flats,
                cb_kwargs={'flat_data': item},
            )
            yield req

    def parse_flats(self, response, flat_data: dict):
        loader = ItemLoader(item=FlatItem(), response=response)

        # Values from previous json response
        loader.add_value('source_id', flat_data.get('id', ""))
        loader.add_value('title', flat_data.get('c', ''))
        loader.add_value('rent', flat_data.get('p', ''))
        loader.add_value('expenses', flat_data.get('p', ''))
        loader.add_value(
            'url', f'https://{self.allowed_domains[0]}/{flat_data.get("u", "")}'
        )
        loader.add_value('lat', flat_data.get('lt'))
        loader.add_value('lon', flat_data.get('ln'))
        loader.add_value('address', flat_data.get('a', ""))
        loader.add_value('nb_rooms', flat_data.get('nr'))
        loader.add_value('nb_bathrooms', flat_data.get('nb', 1))
        loader.add_value('nb_bedrooms', flat_data.get('nsr'))
        loader.add_value('surface', flat_data.get('s'))
        loader.add_value('nb_pics', flat_data.get('pc'))
        loader.add_value('pics', flat_data.get('m', list()))

        # Values scraped from current response web-page
        # loader.add_css('ref')
        # loader.add_css('floor')
        # loader.add_css('availability')

        return loader.load_item()

        # yield {
        #     'source_id': str(flat_data.get('id')),
        #     'title': flat_data.get('c', '').strip(),
        #     'rent': int(match_rent.group(0).replace("'", '')) if match_rent else None,
        #     'expenses': int(match_expenses.group(0).replace('+ ', ''))
        #     if match_expenses
        #     else None,
        #     'url': f'https://{self.allowed_domains[0]}/{flat_data.get("u", "")}',
        #     'lat': flat_data.get('lt'),
        #     'lon': flat_data.get('ln'),
        #     'address': flat_data.get('a', "").strip(),
        #     'nb_rooms': flat_data.get('nr'),
        #     'nb_bathrooms': 1 if flat_data.get('nb', 1) < 1 else flat_data.get('nb', 1),
        #     'nb_bedrooms': flat_data.get('nsr'),
        #     'surface': flat_data.get('s'),
        #     'nb_pics': flat_data.get('pc'),
        #     'pics': flat_data.get('m', list()),
        # }
