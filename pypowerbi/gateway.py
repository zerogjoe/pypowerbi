# -*- coding: future_fstrings -*-
import json

from .encrypt import PublicKey


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

    def encrypted_credential_details(self, **kwargs):
        return CredentialDetails(public_key=self.public_key, **kwargs)

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
            gateway_annotation = json.loads(
                dictionary[Gateway.gateway_annotation_key]
            )
        else:
            gateway_annotation = None

        # gateway_status is optional
        if Gateway.gateway_status_key in dictionary:
            gateway_status = str(dictionary[Gateway.gateway_status_key])
        else:
            gateway_status = None

        # public_key is optional
        if Gateway.public_key_key in dictionary:
            public_key = PublicKey(dictionary[Gateway.public_key_key])
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


class GatewayDatasource:
    # json keys
    id_key = 'id'
    name_key = 'datasourceName'
    basic_credentials_key = 'basicCredentials'
    connection_details_key = 'connectionDetails'
    credential_type_key = 'credentialType'
    credential_details_key = 'credentialDetails'
    datasource_type_key = 'datasourceType'

    def __init__(
        self,
        name,
        datasource_id=None,
        basic_credentials=None,
        connection_details=None,
        credential_type=None,
        credential_details=None,
        datasource_type=None
    ):
        self.name = name
        self.id = datasource_id
        self.basic_credentials = basic_credentials
        self.connection_details = connection_details
        self.credential_type = credential_type
        self.credential_details = credential_details
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
        if GatewayDatasource.id_key in dictionary:
            datasource_id = str(dictionary[GatewayDatasource.id_key])
            # id cannot be whitespace
            if datasource_id.isspace():
                raise RuntimeError('Dataset dict has empty id key value')
        else:
            raise RuntimeError('Dataset dict has no id key')
        # name is required
        if GatewayDatasource.name_key in dictionary:
            datasource_name = str(dictionary[GatewayDatasource.name_key])
            # name cannot be whitespace
            if datasource_name.isspace():
                raise RuntimeError('Dataset dict has empty name key value')
        else:
            raise RuntimeError('Dataset dict has no name key')

        # basic_credentials is optional
        if GatewayDatasource.basic_credentials_key in dictionary:
            basic_credentials = str(
                dictionary[GatewayDatasource.basic_credentials_key])
        else:
            basic_credentials = None

        # connection_details is optional
        if GatewayDatasource.connection_details_key in dictionary:
            connection_details = str(
                dictionary[GatewayDatasource.connection_details_key]
            )
        else:
            connection_details = None

        # credential_type is optional
        if GatewayDatasource.credential_type_key in dictionary:
            credential_type = str(dictionary[GatewayDatasource.credential_type_key])
        else:
            credential_type = None

        # datasource_type is optional
        if GatewayDatasource.datasource_type_key in dictionary:
            datasource_type = str(dictionary[GatewayDatasource.datasource_type_key])
        else:
            datasource_type = None

        return GatewayDatasource(
            datasource_name,
            datasource_id,
            basic_credentials=basic_credentials,
            connection_details=connection_details,
            credential_type=credential_type,
            datasource_type=datasource_type
        )


class GatewayDatasourceEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            GatewayDatasource.datasource_type_key: o.datasource_type,
            GatewayDatasource.connection_details_key: json.dumps(
                o.connection_details,
                separators=(',', ':')),
            GatewayDatasource.name_key: o.name,
            GatewayDatasource.credential_details_key: (
                CredentialDetailsEncoder().default(o.credential_details))
        }


class CredentialDetails:
    # json keys
    credential_type_key = 'credentialType'
    credentials_key = 'credentials'
    encrypted_connection_key = 'encryptedConnection'
    encryption_algorithm_key = 'encryptionAlgorithm'
    privacy_level_key = 'privacyLevel'
    use_caller_aad_identity_key = 'useCallerAADIdentity'
    use_end_user_oauth2_credentials_key = 'useEndUserOAuth2Credentials'
    credential_details_key = 'credentialDetails'
    credential_data_key = 'credentialData'

    def __init__(
        self,
        credential_type=None,
        credentials=None,
        encrypted_connection=None,
        encryption_algorithm=None,
        privacy_level=None,
        use_caller_aad_identity=None,
        use_end_user_oauth2_credentials=None,
        public_key=None
    ):
        self.credential_type = credential_type
        self.credentials = credentials
        self.encrypted_connection = encrypted_connection
        self.encryption_algorithm = encryption_algorithm
        self.use_caller_aad_identity = use_caller_aad_identity
        self.privacy_level = privacy_level
        self.use_end_user_oauth2_credentials = use_end_user_oauth2_credentials
        self.public_key = public_key

    @property
    def encrypted_credentials(self):
        return self.public_key.encrypt(
            json.dumps(
                {self.credential_data_key: self._credential_data},
                separators=(',', ':')
            )
        )

    @property
    def _credential_data(self):
        if self.credentials:
            return [
                {"name": k, "value": v}
                for k, v in self.credentials.items()
            ]
        else:
            return ""


class CredentialDetailsEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            CredentialDetails.credential_type_key: o.credential_type,
            CredentialDetails.credentials_key: o.encrypted_credentials,
            CredentialDetails.encrypted_connection_key: o.encrypted_connection,
            CredentialDetails.encryption_algorithm_key: o.encryption_algorithm,
            CredentialDetails.use_caller_aad_identity_key: (
                o.use_caller_aad_identity
            ),
            CredentialDetails.privacy_level_key: o.privacy_level,
            CredentialDetails.use_end_user_oauth2_credentials_key: (
                o.use_end_user_oauth2_credentials
            )
        }

    def update_datasource(self, o):
        return {
            CredentialDetails.credential_details_key: self.default(o)
        }
