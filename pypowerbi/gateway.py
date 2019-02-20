# -*- coding: future_fstrings -*-
import json


class Gateway:
    # json keys
    id_key = 'id'
    name_key = 'name'
    gateway_annotation_key = 'gatewayAnnotation'
    gateway_status_key = 'gatewayStatus'
    public_key_key = 'publicKey'
    type_key = 'type'

    def __init__(
        self,
        name,
        gateway_id=None,
        gateway_annotation=None,
        gateway_status=None,
        public_key=None,
        type=None
    ):
        self.name = name
        self.id = gateway_id
        self.gateway_annotation = gateway_annotation
        self.gateway_status = gateway_status
        self.public_key = public_key
        self.type = type

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a dataset from a dictionary,
        key values for 'id' and 'name' required
        :param dictionary: The dictionary to create the dataset from
        :return: A dataset created from the given dictionary
        """
        # id is required
        if Gateway.id_key in dictionary:
            gateway_id = str(dictionary[Gateway.id_key])
            # id cannot be whitespace
            if gateway_id.isspace():
                raise RuntimeError('Dataset dict has empty id key value')
        else:
            raise RuntimeError('Dataset dict has no id key')
        # name is required
        if Gateway.name_key in dictionary:
            gateway_name = str(dictionary[Gateway.name_key])
            # name cannot be whitespace
            if gateway_name.isspace():
                raise RuntimeError('Dataset dict has empty name key value')
        else:
            raise RuntimeError('Dataset dict has no name key')

        # gateway_annotation is optional
        if Gateway.gateway_annotation_key in dictionary:
            gateway_annotation = str(
                dictionary[Gateway.gateway_annotation_key])
        else:
            gateway_annotation = None

        # gateway_status is optional
        if Gateway.gateway_status_key in dictionary:
            gateway_status = str(dictionary[Gateway.gateway_status_key])
        else:
            gateway_status = None

        # public_key is optional
        if Gateway.public_key_key in dictionary:
            public_key = str(dictionary[Gateway.public_key_key])
        else:
            public_key = None

        # type is optional
        if Gateway.type_key in dictionary:
            type = str(dictionary[Gateway.type_key])
        else:
            type = None

        return Gateway(
            gateway_name,
            gateway_id,
            gateway_annotation=gateway_annotation,
            gateway_status=gateway_status,
            public_key=public_key,
            type=type
        )


class GatewayEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            Gateway.name_key: o.name
        }


class Datasource:
    # json keys
    id_key = 'id'
    name_key = 'datasourceName'
    basic_credentials_key = 'basicCredentials'
    connection_details_key = 'connectionDetails'
    credential_type_key = 'credentialType'
    datasource_type_key = 'datasourceType'

    def __init__(
        self,
        name,
        datasource_id=None,
        basic_credentials=None,
        connection_details=None,
        credential_type=None,
        datasource_type=None
    ):
        self.name = name
        self.id = datasource_id
        self.basic_credentials = basic_credentials
        self.connection_details = connection_details
        self.credential_type = credential_type
        self.datasource_type = datasource_type

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a dataset from a dictionary,
        key values for 'id' and 'name' required
        :param dictionary: The dictionary to create the dataset from
        :return: A dataset created from the given dictionary
        """
        # id is required
        if Datasource.id_key in dictionary:
            datasource_id = str(dictionary[Datasource.id_key])
            # id cannot be whitespace
            if datasource_id.isspace():
                raise RuntimeError('Dataset dict has empty id key value')
        else:
            raise RuntimeError('Dataset dict has no id key')
        # name is required
        if Datasource.name_key in dictionary:
            datasource_name = str(dictionary[Datasource.name_key])
            # name cannot be whitespace
            if datasource_name.isspace():
                raise RuntimeError('Dataset dict has empty name key value')
        else:
            raise RuntimeError('Dataset dict has no name key')

        # basic_credentials is optional
        if Datasource.basic_credentials_key in dictionary:
            basic_credentials = str(
                dictionary[Datasource.basic_credentials_key])
        else:
            basic_credentials = None

        # connection_details is optional
        if Datasource.connection_details_key in dictionary:
            connection_details = str(
                dictionary[Datasource.connection_details_key]
            )
        else:
            connection_details = None

        # credential_type is optional
        if Datasource.credential_type_key in dictionary:
            credential_type = str(dictionary[Datasource.credential_type_key])
        else:
            credential_type = None

        # datasource_type is optional
        if Datasource.datasource_type_key in dictionary:
            datasource_type = str(dictionary[Datasource.datasource_type_key])
        else:
            datasource_type = None

        return Datasource(
            datasource_name,
            datasource_id,
            basic_credentials=basic_credentials,
            connection_details=connection_details,
            credential_type=credential_type,
            datasource_type=datasource_type
        )


class DatasourceEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            Datasource.name_key: o.name
        }
