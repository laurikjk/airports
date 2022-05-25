import random
import requests
import string
import pandas as pd
from bs4 import BeautifulSoup

A_TO_Z_UPPERCASE = string.ascii_uppercase[:26]

HEADERS = {
    'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
    'Accept-Language': 'en-US, en;q=0.5'
}

def find_column_names(url_prefix, letter):
    page = requests.get(f'{url_prefix}_{letter}', headers=HEADERS)
    th_elems = (
        BeautifulSoup(page.content, features="lxml")
            .find('table')
            .find('tr')
            .find_all('th')
    )
    return [th.text.strip() for th in th_elems]

def scrape_airports_by_iata(url_prefix):
    columns = find_column_names(url_prefix, A_TO_Z_UPPERCASE[0])

    data = pd.DataFrame(columns=columns)

    for letter in A_TO_Z_UPPERCASE:
        page = requests.get(
            f'{url_prefix}_{letter}',
            headers=HEADERS
        )
        rows = (
            BeautifulSoup(page.content, features="lxml")
                .find('table')
                .find_all('tr')
        )
        for row in rows:
            cell_values = [cell.text.strip() for cell in row.find_all('td')]
            if cell_values and len(cell_values) == len(columns):
                data = data.append(pd.Series(cell_values, index=columns), ignore_index=True)
    return data

            
    