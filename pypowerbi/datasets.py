# -*- coding: future_fstrings -*-
import requests
import json

from requests.exceptions import HTTPError
from .dataset import *
from .datasource import *
from .gateways import Gateways


class Datasets:
    # url snippets
    groups_snippet = 'groups'
    datasets_snippet = 'datasets'
    tables_snippet = 'tables'
    rows_snippet = 'rows'
    parameters_snippet = 'parameters'
    refreshes_snippet = 'refreshes'
    datasources_snippet = 'datasources'
    update_datasources_snippet = 'Default.UpdateDatasources'

    # json keys
    get_datasets_value_key = 'value'
    get_datasources_value_key = 'value'
    update_details_key = 'updateDetails'
    datasource_selector_key = 'datasourceSelector'
    connection_details_key = 'connectionDetails'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def count(self, group_id=None):
        """
        Evaluates the number of datasets
        :param group_id: The optional group id
        :return: The number of datasets as returned by the API
        """
        return len(self.get_datasets(group_id))

    def has_dataset(self, dataset_id, group_id=None):
        """
        Evaluates if the dataset exists
        :param dataset_id: The id of the dataset to evaluate
        :param group_id: The optional group id
        :return: True if the dataset exists, False otherwise
        """
        datasets = self.get_datasets(group_id)

        for dataset in datasets:
            if dataset.id == str(dataset_id):
                return True

        return False

    def get_datasets(self, group_id=None):
        """
        Fetches all datasets
        https://msdn.microsoft.com/en-us/library/mt203567.aspx
        :param group_id: The optional group id to get datasets from
        :return: The list of the datasets found
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasets request returned http error: {response.json()}')

        return self.datasets_from_get_datasets_response(response)

    def get_dataset(self, dataset_id, group_id=None):
        """
        Gets a single dataset
        https://msdn.microsoft.com/en-us/library/mt784653.aspx
        :param dataset_id: The id of the dataset to get
        :param group_id: The optional id of the group to get the dataset from
        :return: The dataset returned by the API
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}'
        # form the headers
        headers = self.client.auth_header
        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasets request returned http error: {response.json()}')

        return Dataset.from_dict(json.loads(response.text))

    def post_dataset(self, dataset, group_id=None):
        """
        Posts a single dataset
        https://msdn.microsoft.com/en-us/library/mt203562.aspx
        :param dataset: The dataset to push
        :param group_id: The optional group id to push the dataset to
        :return: The pushed dataset as returned by the API
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}'
        # form the headers
        headers = self.client.auth_header
        # form the json dict
        json_dict = DatasetEncoder().default(dataset)

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 201 - Created. The request was fulfilled and a new Dataset was created.
        if response.status_code != 201:
            raise HTTPError(response, f'Post Datasets request returned http code: {response.json()}')

        return Dataset.from_dict(json.loads(response.text))

    def delete_dataset(self, dataset_id, group_id=None):
        """
        Deletes a dataset
        :param dataset_id: The id of the dataset to delete
        :param group_id: The optional group id to delete the dataset from
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.delete(url, headers=headers)

        # 200 is the only successful code
        if response.status_code != 200:
            raise HTTPError(response, f'Delete Dataset request returned http error: {response.json()}')

    def delete_all_datasets(self, group_id=None):
        """
        Deletes all datasets
        :param group_id: The optional group id of the group to delete all datasets from
        """
        # get all the datasets and delete each one
        datasets = self.get_datasets(group_id)
        for dataset in datasets:
            self.delete_dataset(group_id, dataset.id)

    def get_tables(self, dataset_id, group_id=None):
        """
        Gets tables from a dataset
        https://msdn.microsoft.com/en-us/library/mt203556.aspx
        :param dataset_id: The id of the dataset which to get tables from
        :param group_id: The optional id of the group which to get tables from
        :return: A list of tables from the given group and dataset
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}/{self.tables_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasets request returned http error: {response.json()}')

        return self.tables_from_get_tables_response(response)

    def post_rows(self, dataset_id, table_name, rows, group_id=None):
        """
        Posts rows to a table in a given dataset
        https://msdn.microsoft.com/en-us/library/mt203561.aspx
        :param dataset_id: The id of the dataset to post rows to
        :param table_name: The name of the table to post rows to
        :param rows: The rows to post to the table
        :param group_id: The optional id of the group to post rows to
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}/' \
              f'{self.tables_snippet}/{table_name}/{self.rows_snippet}'
        # form the headers
        headers = self.client.auth_header
        # form the json dict
        row_encoder = RowEncoder()
        json_dict = {
            'rows': [row_encoder.default(x) for x in rows]
        }

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 is the only successful code
        if response.status_code != 200:
            raise HTTPError(response, f'Post row request returned http error: {response.json()}')

    def delete_rows(self, dataset_id, table_name, group_id=None):
        """
        Deletes all rows from a table in a given dataset
        https://msdn.microsoft.com/en-us/library/mt238041.aspx
        :param dataset_id: The id of the dataset to delete the rows from
        :param table_name: The name of the table to delete the rows from
        :param group_id: The optional id of the group to delete the rows from
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}/' \
              f'{self.tables_snippet}/{table_name}/{self.rows_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.delete(url, headers=headers)

        # 200 is the only successful code
        if response.status_code != 200:
            raise HTTPError(response, f'Post row request returned http error: {response.json()}')

    def get_dataset_parameters(self, dataset_id, group_id=None):
        """
        Gets all parameters for a single dataset
        https://msdn.microsoft.com/en-us/library/mt784653.aspx
        :param dataset_id: The id of the dataset from which you want the parameters
        :param group_id: The optional id of the group to get the dataset's parameters
        :return: The dataset parameters returned by the API
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}/{self.parameters_snippet}'
        # form the headers
        headers = self.client.auth_header
        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Dataset parameters request returned http error: {response.json()}')

        return json.loads(response.text)

    def refresh_dataset(self, dataset_id, notify_option=None, group_id=None):
        """
        Refreshes a single dataset
        :param dataset_id: The id of the dataset to refresh
        :param notify_option: The optional notify_option to add in the request body
        :param group_id: The optional id of the group
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}/{self.datasets_snippet}/{dataset_id}/{self.refreshes_snippet}'

        # form the headers
        headers = self.client.auth_header

        if notify_option is not None:
            json_dict = {
                'notifyOption': notify_option
            }
        else:
            json_dict = None

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 202:
            raise HTTPError(response, f'Refresh dataset request returned http error: {response.json()}')

    def get_datasources(self, dataset_id, group_id=None):
        """
        Fetches all datasources for a dataset
        https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/getdatasources
        :param dataset_id: The dataset id to get datasources from
        :param group_id: The optional group id where the dataset is published
        :return: The list of the datasources found
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = (
            f'{self.base_url}{groups_part}/'
            f'{self.datasets_snippet}/'
            f'{dataset_id}/'
            f'{self.datasources_snippet}'
        )
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasources request returned http error: {response.json()}')

        return Gateways.datasources_from_get_datasources_response(response)

    def update_datasources(self, update_instructions, dataset_id, group_id=None):
        """
        Fetches all datasources for a dataset
        https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/updatedatasources
        https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/updatedatasourcesingroup
        :param update_instructions: List of (Datasource, ConnectionDetails)
                                    tuples where Datasource is a selector and
                                    ConnectionDetails contains the new
                                    connection details
        :param dataset_id: The dataset id to update datasources in
        :param group_id: The optional group id where the dataset is published
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = (
            f'{self.base_url}{groups_part}/'
            f'{self.datasets_snippet}/'
            f'{dataset_id}/'
            f'{self.update_datasources_snippet}'
        )
        # form the headers
        headers = self.client.auth_header

        datasource_encoder = DatasourceEncoder()
        connection_details_encoder = ConnectionDetailsEncoder()

        json_dict = {
            self.update_details_key: [
                {
                    self.datasource_selector_key: (
                        datasource_encoder.update_datasources(
                            datasource_selector)),
                    self.connection_details_key: (
                        connection_details_encoder.default(
                            connection_details))
                }
                for datasource_selector, connection_details
                in update_instructions
            ]
        }
        print(json_dict)

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Update Datasources request returned http error: {response.json()}')

    @classmethod
    def datasets_from_get_datasets_response(cls, response):
        """
        Creates a list of datasets from a http response object
        :param response: The http response object
        :return: A list of datasets created from the given http response object
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        datasets = []
        # go through entries returned from API
        for entry in response_dict[cls.get_datasets_value_key]:
            datasets.append(Dataset.from_dict(entry))

        return datasets

    @classmethod
    def tables_from_get_tables_response(cls, response):
        """
        Creates a list of tables from a http response object
        :param response: The http response object
        :return: A list of tables created from the given http response object
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        tables = []
        # go through entries returned from API
        for entry in response_dict[cls.get_datasets_value_key]:
            tables.append(Table.from_dict(entry))

        return tables
