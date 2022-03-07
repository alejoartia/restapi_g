import json
from typing import List
import requests as _resquests 
import app.config as cfg

def _generate_url() -> str:
    url = f"{cfg.BASE_URL_BANXICO}v1/series/SF43718/datos/oportuno?token={cfg.API_TOKEN_BANXICO}"
    return url


def _get_page(url:str) -> str:
    response =_resquests.get(url)
    return response.json()


def currency_of_the_day() -> str:
    """
    Return the currency of the day 
    """
    url = _generate_url()
    page = _get_page(url)

    data = page['bmx']['series'][0]['datos'][0]
    convert = {'last_updated': data['fecha'], 'value': float(data['dato'])}

    return convert 


currency_of_the_day()
