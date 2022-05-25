from scrape_airports import scrape_airports, scrape_airports_by_iata

def main():
    airports = scrape_airports_by_iata('https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:')
    airports_missing_icao = airports[airports['ICAO'] == '']
    print(f'{len(airports)} airports scraped')
    print(f'{len(airports_missing_icao)} airports missing ICAO codes')
    print('Writing to airports.csv')
    airports.to_csv('data/airports.csv')
    print('Writing to airports_missing_icao.csv')
    airports_missing_icao.to_csv('data/airports_missing_icao.csv')

main()