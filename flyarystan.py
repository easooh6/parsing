import requests

# Flight search parameters as dictionary
search_params = {
    'searchGroupId': 'standard',
    'segmentsCount': 2,
    'date[0]': '28.05.2025',
    'origin-city-code[0]': 'ALA',
    'destination-city-code[0]': 'NQZ',
    'date[1]': '06.07.2025',
    'origin-city-code[1]': 'NQZ',
    'destination-city-code[1]': 'ALA',
    'adultsCount': 1,
    'childrenCount': 0,
    'childCount': 0,
    'infantsWithSeatCount': 0,
    'infantsWithoutSeatCount': 0,
    'lang': 'ru',
    'currency': 'KZT'
}

# Make POST request with data parameter
response = requests.post(
    'https://booking.flyqazaq.com/websky/json/cartesian-search-period',
    data=search_params
)

print(response.status_code)
print(response.text)