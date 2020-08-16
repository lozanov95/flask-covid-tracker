import requests
import re


class CaseScrapper:
    def __init__(self):
        self.cases, self.tests = self.scrape()

    @staticmethod
    def scrape_new_cases(text):
        table = text.split('<table class="table">')
        table = table[2]
        numbers = re.findall(r'>([0-9]+)<', table)
        new_cases = int(numbers[len(numbers) - 1])
        return new_cases

    @staticmethod
    def scrape_new_tests(text):
        table = text.split('<p class')
        new_tests = int(re.search(r'[0-9\s]+', table[3]).group().replace(' ', ''))
        return new_tests

    def scrape(self):
        url = 'https://coronavirus.bg/bg/statistika'
        r = requests.get(url).content.decode('utf-8')
        new_cases = self.scrape_new_cases(r)
        new_tests = self.scrape_new_tests(r)
        return new_cases, new_tests

    def get_stats(self):
        return self.cases, self.tests
