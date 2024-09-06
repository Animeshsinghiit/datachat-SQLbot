"""
Data IO helper for Google Big Query
"""
from google.cloud import bigquery
from google.oauth2 import service_account


class BigQueryData:
    """
    Fetch data from Google BigQuery via Native GBQ client or pandas
    """

    def __init__(self, cred_info, schema, location=None):
        """
        :param cred_info: Connection credentials. Should contain the following keys
            ['type', 'project_id', 'private_key_id', 'private_key', 'client_email',
             'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
             'client_x509_cert_url']
        :type cred_info: dict
        """
        self.cred_info = cred_info
        self.schema = schema
        self.project = cred_info.get('project_id')
        self.location = location

    def get_credentials(self):
        """
        Create credential object
        """
        return service_account.Credentials.from_service_account_info(self.cred_info)

    def get_connection_client(self):
        """
        Create Google big query connection client with credentials
        """
        storage_credentials = self.get_credentials()
        return bigquery.Client(project=self.project,
                               credentials=storage_credentials,
                               location=self.location)

    def read_data_gbq_native_client(self, query):
        """
        Read data from native google bg client method

        :param table_name: table alias
        :type table_name: str

        :return: table data
        :rtype: pd.DataFrame
        """
        client = self.get_connection_client()
        return client.query(query).to_dataframe()
