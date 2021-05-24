"""
    download_raids
    ==============

    generates static files in /data with format
    {
        the Labyrinth of the Ancients: raid,

"""

import requests
import time
import json

TRIAL = 4  # both normal and extreme
RAIDS = 5
ULTIMATE_RAIDS = 28


def get_all_pages(url):
    results = []
    i = 1
    while True:
        content = requests.get(url, params={'page': i}).json()
        results += content['Results']
        if content['Pagination']['PageNext'] is None:
            print(f'Consumed all content on page {i}')
            return results
        i += 1
        time.sleep(1)


result = {}
if __name__ == '__main__':

    for id_, name in [(TRIAL, 'Trial'), (RAIDS, 'Raid'), (ULTIMATE_RAIDS, 'UltimateRaid')]:
        url = f"https://xivapi.com/search?filters=ContentType.ID={id_}"

        for element in get_all_pages(url):
            result[element['Name']] = name

    with open('../data/encounters.json', 'w') as fo:
        json.dump(result, fo, indent=2, sort_keys=True)
