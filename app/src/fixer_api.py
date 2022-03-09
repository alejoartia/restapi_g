from typing import List
from urllib import response
import requests as _resquests 
import json 
import app.config as cfg


def _generate_url() -> str:
    url = f"{cfg.BASE_URL_FIXER}={cfg.API_KEY_FIXER}"
    return url


def _get_page(url:str) -> str:
    response =_resquests.get(url)
    return response.json()


def currency_of_the_day() -> List[str]:
    """
    Return the currency of the day  
    """
    url = _generate_url()
    data = _get_page(url)
    time = data['date']
    usd = data['rates']['USD']
    eur = data['rates']['EUR'] #the base should return 1 
    mxn = data['rates']['MXN']

    #As the free account only let get the currency based on EUR 
    #it's needed an ajustment with MXN and USD 
    usd_mxn = mxn/usd
    convert = {'last_updated': time, 'value': usd_mxn}
    
    return convert

currency_of_the_day()