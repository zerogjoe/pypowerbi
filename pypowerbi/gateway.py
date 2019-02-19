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
        table_encoder = TableEncoder()

        json_dict = {
            Gateway.name_key: o.name,
            Gateway.tables_key: [table_encoder.default(x) for x in o.tables],
        }

        return json_dict
