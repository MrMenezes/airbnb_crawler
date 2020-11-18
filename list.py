import requests
import json
from bs4 import BeautifulSoup
import sys

adults = 2
check_in = '2021-05-10'
check_out = '2021-05-12'


def total(id_value, check_in, check_out):
    headers = {
        'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'x-airbnb-graphql-platform': 'web',
    }

    params = (
        ('operationName', 'PdpPlatformSections'),
        ('locale', 'pt'),
        ('currency', 'BRL'),
        ('variables', '{"request":{"id":"'+id_value +
         '","layouts":[],"sectionIds":["BOOK_IT_SIDEBAR"],"checkIn":"'+check_in+'","checkOut":"'+check_out+'"}}'),
        ('extensions',
         '{"persistedQuery":{"version":1,"sha256Hash":"c4e4690265fdbd38d7819a8eb702dde2d92398761ae85881c62bd04e0585491b"}}'),
    )

    response = requests.get(
        'https://www.airbnb.com.br/api/v3/PdpPlatformSections', headers=headers, params=params)

    data_json = json.loads(response.text)
    section = data_json['data']['merlin']['pdpSections']['sections'][0]

    total = section['section']['price']['total']['amount']
    return total


def get_wishlists(wishlists, check_in, check_out, adults):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }

    response = requests.get(
        'https://www.airbnb.com.br/wishlists/{wishlists}'.format(wishlists=wishlists), headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    data_soup = soup.find('script', id='data-state')
    data_json = json.loads(data_soup.string)
    items = data_json['niobeMinimalClientData'][0][1]['data']['presentation'][
        'wishlistDetailPage']['wishlistDetailPage']['sections'][0]['section']['items']

    items_data = []
    for item in items:
        simple_data = {}
        item_id = item['listing']['id'],
        simple_data['bathrooms'] = item['listing']['bathrooms']
        simple_data['beds'] = item['listing']['beds']
        simple_data['bedrooms'] = item['listing']['bedrooms']
        simple_data['city'] = item['listing']['city']
        simple_data['name'] = item['listing']['name']
        simple_data['personCapacity'] = item['listing']['personCapacity']
        simple_data['pictureUrl'] = item['listing']['pictureUrl']
        simple_data['publicAddress'] = item['listing']['publicAddress']
        simple_data['spaceType'] = item['listing']['spaceType']
        simple_data['url'] = 'https://www.airbnb.com.br/rooms/{id}?adults={adults}&check_in={check_in}&check_out={check_out}'.format(
            id=item_id[0], adults=adults, check_in=check_in, check_out=check_out)
        simple_data['total'] = total(item_id[0], check_in, check_out)
        simple_data['id'] = item_id[0]
        items_data.append(simple_data)
    return items_data


wishlists = 867287597 if len(sys.argv) < 2 else sys.argv[1]

print(json.dumps(get_wishlists(wishlists, check_in,
                               check_out, adults), sort_keys=True, indent=4))