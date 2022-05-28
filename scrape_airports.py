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

def elements_to_text(elements):
    return [element.text.strip() for element in elements]

def find_table_cell_values(page, cell_amnt):
    soup = BeautifulSoup(page.content, features="lxml")
    rows = soup.find('table').find_all('tr')
    cells_as_arrays = [row.find_all('td') for row in rows]
    return [elements_to_text(cell_array)
        for cell_array
        in cells_as_arrays
        if cell_array
        and len(cell_array) == cell_amnt]

def scrape_airports_by_iata(url_prefix):
    columns = find_column_names(url_prefix, A_TO_Z_UPPERCASE[0])

    data = pd.DataFrame(columns=columns)

    for letter in A_TO_Z_UPPERCASE:
        page = requests.get(
            f'{url_prefix}_{letter}',
            headers=HEADERS
        )
        df = pd.DataFrame(
            find_table_cell_values(page, len(columns)),
            columns=columns
        )
        data = data.append(df, ignore_index=True)
    return data
