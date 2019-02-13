"""

AUTHOR: Juanjo

DATE: 07/02/2019

"""

import requests


class AEMETError(Exception):
    pass


class AEMETClient:
    """
    A class representing the AEMET API entry point. Every request to the
    API is done programmatically via a concrete instance of this class.

    The class provides methods for differents API endpoints.

    :param str api_key: API key to get access to AEMET API
    :returns: an *AEMETClient* instance

    """

    CONVERSATIONAL_OBSERVATION_URL = 'https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{}'

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_conventional_observation(self, station_id):
        """
        Returns weather information for conventional observation.

        :returns: a dict with weather info
        :raises: *AEMETError* if there are any problems during the request.

        """

        url = self.CONVERSATIONAL_OBSERVATION_URL.format(station_id)
        querystring = {'api_key': self.api_key}
        headers = {
            'cache-control': 'no-cache'
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
        except requests.exceptions.RequestException as re:
            raise AEMETError('An error ocurred fetching conversational observation', re)
        if response.status_code != 200:
            raise AEMETError(response.text)
        data = response.json()
        # Retrieve the temporary URL from which to request the data
        data_url = data['datos']
        try:
            response = requests.get(data_url)
        except requests.exceptions.RequestException as re:
            raise AEMETError('An error ocurred fetching conversational observation data', re)
        if response.status_code != 200:
            raise AEMETError(response.text)
        return response.json()
