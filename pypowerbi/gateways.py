# -*- coding: future_fstrings -*-
import requests
import json

from requests.exceptions import HTTPError
from .gateway import *
from .datasource import *


class Gateways:
    # url snippets
    gateways_snippet = 'gateways'
    datasources_snippet = 'datasources'

    # json keys
    get_gateways_value_key = 'value'
    get_datasources_value_key = 'value'

    def __init__(self, client):
        self.client = client
        self.base_url = (
            f'{self.client.api_url}/'
            f'{self.client.api_version_snippet}/'
            f'{self.client.api_myorg_snippet}'
        )

    def get_gateways(self):
        """
        Fetches all gateways
        https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/getgateways
        :return: The list of the gateways found
        """

        # form the url
        url = f'{self.base_url}/{self.gateways_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code,
        # raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(
                response,
                f'Get Datasets request returned http error: {response.json()}'
            )

        return self.gateways_from_get_gateways_response(response)

    def get_datasources(self, gateway_id):
        """
        Fetches all datasources
        https://docs.microsoft.com/en-us/rest/api/power-bi/datasources/getdatasources
        :return: The list of the datasources found
        """

        # form the url
        url = (
            f'{self.base_url}/'
            f'{self.gateways_snippet}/'
            f'{gateway_id}/'
            f'{self.datasources_snippet}'
        )
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code,
        # raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(
                response,
                f'Get Datasets request returned http error: {response.json()}'
            )

        return self.datasources_from_get_datasources_response(response)

    def create_datasource(self, datasource, gateway_id):
        """
        Creates a single datasource
        https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/createdatasource
        :param datasource: The datasource to create
        :param gateway_id: The gateway id to create the datasource in
        :return: True
        """

        # form the url
        url = (
            f'{self.base_url}/'
            f'{self.gateways_snippet}/'
            f'{gateway_id}/'
            f'{self.datasources_snippet}'
        )
        # form the headers
        headers = self.client.auth_header
        # form the json dict
        json_dict = DatasourceEncoder().default(datasource)

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 201 - Created. The request was fulfilled and a new Dataset was created.
        if response.status_code != 201:
            raise HTTPError(response, f'Create Datasource request returned http code: {response.json()}')

        return True

    def update_datasource(self, credential_details, gateway_id, datasource_id):
        """
        Updates the credentials of the specified datasource from the
        specified gateway.
        https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/updatedatasource
        :param credential_details: The new credential details
        :param gateway_id: The gateway id to update the datasource in
        :param datasource_id: The datasource id to update
        :return: True
        """

        # form the url
        url = (
            f'{self.base_url}/'
            f'{self.gateways_snippet}/'
            f'{gateway_id}/'
            f'{self.datasources_snippet}/'
            f'{datasource_id}'
        )
        # form the headers
        headers = self.client.auth_header
        # form the json dict
        json_dict = CredentialDetailsEncoder().update_datasource(
            credential_details
        )

        # get the response
        response = requests.patch(url, headers=headers, json=json_dict)

        # 200 - OK. The request was fulfilled and the credentials were updated.
        if response.status_code != 200:
            raise HTTPError(response, f'Update Datasource request returned http code: {response.json()}')

        return True

    @classmethod
    def gateways_from_get_gateways_response(cls, response):
        """
        Creates a list of gateways from a http response object
        :param response: The http response object
        :return: A list of gateways created from the given http response object
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        # go through entries returned from API
        return [
            Gateway.from_dict(entry)
            for entry in response_dict[cls.get_gateways_value_key]
        ]

    @classmethod
    def datasources_from_get_datasources_response(cls, response):
        """
        Creates a list of datasources from a http response object
        :param response: The http response object
        :return: A list of datasources created from the given http response object
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        # go through entries returned from API
        return [
            Datasource.from_dict(entry)
            for entry in response_dict[cls.get_datasources_value_key]
        ]
