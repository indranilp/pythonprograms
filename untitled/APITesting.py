import requests
from requests.exceptions import HTTPError

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred:')  # Python 3.6
    except Exception as err:
        print('Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')