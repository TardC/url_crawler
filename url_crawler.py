'''Crawl the URL of the `target` website.
'''
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class URLCrawler():
    def __init__(self, target):
        self.target = target
        self.old_urls = set()
        self.new_urls = set()
        self.new_urls.add(self.target)

    def _get_new_urls(self, url):
        parsed_target = urlparse(self.target)
        new_urls = []
        response = requests.get(url)
        bs = BeautifulSoup(response.text)

        a_tags = bs.find_all('a')
        for a_tag in a_tags:
            new_url = a_tag.get('href')
            parsed_new_url = urlparse(new_url)
            # Just note the URL of the `target` website.
            if parsed_new_url.netloc == parsed_target.netloc:
                new_urls.append(new_url)
            elif parsed_new_url.scheme == '' and parsed_new_url.netloc == '':
                # Transfrom relative URL to absulote URL.
                full_new_url = urljoin(url, new_url)
                new_urls.append(full_new_url)

        form_tags = bs.find_all('form')
        for form_tag in form_tags:
            new_url = form_tag.get('action')
            parsed_new_url = urlparse(new_url)
            # Just note the URL of the `target` website.
            if parsed_new_url.netloc == parsed_target.netloc:
                new_urls.append(new_url)
            elif parsed_new_url.scheme == '' and parsed_new_url.netloc == '':
                # Transfrom relative URL to absulote URL.
                full_new_url = urljoin(url, new_url)
                new_urls.append(full_new_url)
        return new_urls

    def run(self):
        while True:
            new_url = self.new_urls.pop()
            self.old_urls.add(new_url)
            print("Crawled URL:", new_url)
            urls = self._get_new_urls(new_url)
            for url in urls:
                if url not in self.old_urls:
                    self.new_urls.add(url)

            if len(self.new_urls) == 0:
                break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Crawl urls of the target website')
    parser.add_argument('target', help='The target website, such as http://example.com')

    args = parser.parse_args()
    url_crawler = URLCrawler(args.target)
    url_crawler.run()
    # print(url_crawler.old_urls)
