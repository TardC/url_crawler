"""XSS vulnerability detection.
"""
import random

import requests
from bs4 import BeautifulSoup


class XSSDetection:
    def __init__(self, url):
        self.url = url
        self.vulnerable = False
        self.random_int = random.randint(1000000, 9999999)
        self.payloads = [
            '<scRIPt>%d</scRIPt>' % self.random_int,
            '"><scRIPt>%d</scRIPt>' % self.random_int,
        ]

    def detect(self):
        for payload in self.payloads:
            url = self.url + payload
            response = requests.get(url)
            bs = BeautifulSoup(response.text)
            tag = bs.find('script', text=self.random_int)
            if tag:
                self.vulnerable = True
