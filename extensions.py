import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote_ticker, base_ticker = keys[quote], keys[base]

        if quote == base:
            raise APIException('Невозможная операция (одинаковые валюты)')
        
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неправильная или несуществующая валюта {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неправильная или несуществующая валюта {quote}')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        data = json.loads(r.content)
        total = data[base_ticker] * amount

        return total