import requests
import json


class CaseScrapper:
    def __init__(self):
        self.cases, self.tests = self.scrape()

    def scrape(self):
        url = 'https://coronavirus.bg/stats.json'
        covid_data = json.loads(requests.get(url).content)
        return covid_data['infectedtoday'], covid_data['testedtoday']

    def get_stats(self):
        return self.cases, self.tests
