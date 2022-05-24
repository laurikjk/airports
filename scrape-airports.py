import random
import requests
import string
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = [
    {
        'User-Agent':'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405',
        'Accept-Language': 'en-US, en;q=0.5'
    },
    {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
]

def find_column_names(url, letter):
    page = requests.get(f'{url}_{letter}', headers=HEADERS[0])
    soup = BeautifulSoup(page.content, features="lxml")
    table = soup.find('table')
    return [th.text.strip() for th in table.find('tr').find_all('th')]

def scrape_airports(url):
    a_to_z_uppercase = string.ascii_uppercase[:26]
    columns = find_column_names(url, a_to_z_uppercase[0])
    data = pd.DataFrame(columns=columns)
    for letter in a_to_z_uppercase:
        zero_or_one = random.randint(0, 1)
        page = requests.get(f'{url}_{letter}', headers=HEADERS[zero_or_one])
        soup = BeautifulSoup(page.content, features="lxml")
        table = soup.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cell_values = [cell.text.strip() for cell in row.find_all('td')]
            if cell_values and len(cell_values) == len(columns):
                data = data.append(pd.Series(cell_values, index=columns), ignore_index=True)
    return data

done = scrape_airports("https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:")

print(done)


            
    