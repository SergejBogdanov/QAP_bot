import json
import requests
from config import *


class APIException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не смог обработать валюту "{quote}".')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не смог обработать валюту "{base}".')

        if quote == base:
            raise APIException(
                f'Нельзя перевести одинаковые валюты "{base}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не смог обработать количество "{amount}".')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_base = round((float(json.loads(r.content)[keys[base]]) * amount), 2)

        return total_base
