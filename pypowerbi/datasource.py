import json

class Datasource:
    # json keys
    id_key = 'id'
    id_alternative_key = 'datasourceId'
    name_key = 'datasourceName'
    name_alternative_key = 'name'
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
        Creates a datasource from a dictionary,
        key value for 'name' required
        :param dictionary: The dictionary to create the datasource from
        :return: A datasource created from the given dictionary
        """
        if Datasource.id_key in dictionary:
            datasource_id = str(dictionary[Datasource.id_key])
        elif Datasource.id_alternative_key in dictionary:
            datasource_id = str(dictionary[Datasource.id_alternative_key])
        else:
            datasource_id = None

        # name is required
        if Datasource.name_key in dictionary:
            datasource_name = str(dictionary[Datasource.name_key])
            # name cannot be whitespace
            if datasource_name.isspace():
                raise RuntimeError('Dataset dict has empty name key value')
        elif Datasource.name_alternative_key in dictionary:
            datasource_name = str(dictionary[Datasource.name_alternative_key])
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
            connection_details = dictionary[Datasource.connection_details_key]
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
            Datasource.datasource_type_key: o.datasource_type,
            Datasource.connection_details_key: json.dumps(
                o.connection_details,
                separators=(',', ':')),
            Datasource.name_key: o.name,
            Datasource.credential_details_key: (
                CredentialDetailsEncoder().default(o.credential_details))
        }

    def update_datasources(self, o):
        return {
            Datasource.datasource_type_key: o.datasource_type,
            Datasource.connection_details_key: o.connection_details,
            Datasource.name_key: o.name
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


class ConnectionDetails:
    # json keys
    database_key = 'database'
    server_key = 'server'
    url_key = 'url'

    def __init__(
        self,
        database=None,
        server=None,
        url=None
    ):
        self.database = database
        self.server = server
        self.url = url


class ConnectionDetailsEncoder(json.JSONEncoder):

    def default(self, o):
        return {
            ConnectionDetails.database_key: o.database,
            ConnectionDetails.server_key: o.server,
            ConnectionDetails.url_key: o.url
        }
