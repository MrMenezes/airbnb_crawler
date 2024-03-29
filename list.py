import requests
import json
from bs4 import BeautifulSoup


def get_total(id_value, check_in, check_out, adults, children=0, infants=0):
    headers = {
        'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'x-airbnb-graphql-platform': 'web',
    }

    params = (
        ('operationName', 'PdpPlatformSections'),
        ('locale', 'pt'),
        ('currency', 'BRL'),
        ('variables', '{"request":{"id":"'+str(id_value) +
         '","layouts":[],"adults":"'+str(adults)+'","children":"'+str(children)+'","infants":"'+str(infants)+'","sectionIds":["BOOK_IT_SIDEBAR"],"checkIn":"'+check_in+'","checkOut":"'+check_out+'"}}'),
        ('extensions',
         '{"persistedQuery":{"version":1,"sha256Hash":"c4e4690265fdbd38d7819a8eb702dde2d92398761ae85881c62bd04e0585491b"}}'),
    )

    response = requests.get(
        'https://www.airbnb.com.br/api/v3/PdpPlatformSections', headers=headers, params=params)

    data_json = json.loads(response.text)
    section = data_json['data']['merlin']['pdpSections']['sections'][0]

    total = section['section']['price']['total']['amount']
    disponibility = section['section']['localizedUnavailabilityMessage'] is None
    return {"total": total, "disponibility": disponibility}


def get_wishlists(wishlists, check_in, check_out, adults, total=None, children=0, infants=0):

    response = requests.get(
        'https://www.airbnb.com.br/wishlists/{wishlists}'.format(wishlists=wishlists))

    soup = BeautifulSoup(response.text, 'html.parser')
    data_soup = soup.find('script', id='data-state')
    data_json = json.loads(data_soup.string)
    temp_items = data_json['niobeMinimalClientData'][1][1]['data']['presentation'][
        'wishlistDetailPage']['wishlistDetailPage']['sections']

    items = []
    for temp in temp_items:
        items += temp['section']['items']

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
        simple_data['url'] = 'https://www.airbnb.com.br/rooms/' + item_id[0]
        if total is not None:
            total_item = get_total(
                item_id[0], check_in, check_out, adults, children, infants)
            simple_data['total'] = total_item['total']
            simple_data['disponibility'] = total_item['disponibility']
        simple_data['id'] = item_id[0]
        items_data.append(simple_data)
    return items_data
