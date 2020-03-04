"""SQL injection vulnerability detection.
"""
import random

import requests


class SqliDetection():
    def __init__(self, url, data=None):
        self.url = url
        self.vulnerable = False

        random_int1 = random.randint(1, 1000)
        random_int2 = random_int1 + random.randint(1, 1000)
        self.payloads = {
            'boolean_based': {
                'int': [
                    ' and %d=%d' % (random_int1, random_int1),
                    ' and %d=%d' % (random_int1, random_int2)
                ],
                'quote': [
                    "' and '%d'='%d" % (random_int1, random_int1),
                    "' and '%d'='%d" % (random_int1, random_int2)
                ],
                'double_quote': [
                    '" and "%d"="%d' % (random_int1, random_int1),
                    '" and "%d"="%d' % (random_int1, random_int2)
                ]
            },
            'error_based': {}
        }

    def boolean_based_detect(self):
        payloads = self.payloads['boolean_based']
        for arg_type, payloads in payloads.items():
            url1 = self.url + payloads[0]
            print("Detecting:", url1)
            response1 = requests.get(url1)
            url2 = self.url + payloads[1]
            print("Detecting:", url2)
            response2 = requests.get(url2)
            if response1.text != response2.text:
                self.vulnerable = True


if __name__ == "__main__":
    sqlidetection = SqliDetection('http://testphp.vulnweb.com/listproducts.php?cat=1')
    sqlidetection.boolean_based_detect()
    print(sqlidetection.vulnerable)
