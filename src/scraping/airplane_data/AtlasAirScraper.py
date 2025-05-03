import pandas as pd

from scraping.airplane_data.IIAirScraperScraper import IAirScraper


class AtlasAirScraper(IAirScraper):
    def __init__(self):
        pass

    def getData(self):
        url = 'https://jumpseat.atlasair.com/travel/schedule.asp'
        tables = pd.read_html(url)  # Returns a list of DataFrames
        return tables[0]  # Select the first table

