from typing import List
import requests as _resquests 
import bs4 as _bs4
import app.config as cfg


def _generate_url() -> str:
    url = f"{cfg.BASE_URL_FEDERACION}"
    return url


def _get_page(url:str) -> _bs4.BeautifulSoup:
    page =_resquests.get(url)
    soup = _bs4.BeautifulSoup(page.content, "html.parser")
    return soup


def currency_of_the_day() -> List[str]:
    """
    Return the currency of the day 
    """
    url = _generate_url()
    page = _get_page(url)
    #raw_tittles= page.find_all(class_='renglonPar')

    currency_table = []
    for tr in page.select('tr[align="center"]'):
        new_strings = []
        for td in tr.find_all('td'):
            new_strings.append(td.text.strip())
        currency_table.append(new_strings)

    return currency_table 


def convert_to_dict():
    
    data = currency_of_the_day()
    convert = {'last_updated': data[1][0], 'value': float(data[1][3])}
    #print(conver)
    return convert

convert_to_dict()