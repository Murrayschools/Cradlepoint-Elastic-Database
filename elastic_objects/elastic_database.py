from elasticsearch import Elasticsearch
from typing import Any
from subprocess import run
import logging
import atexit
import json
import os

logger = logging.getLogger(os.environ["LOGGER-NAME"])

class ElasticDatabase:
    def __init__(self):
        self.es_client = Elasticsearch(
            "https://localhost:9200", 
            # ca_certs=f"{os.getcwd()}/http_ca.crt", 
            # ca_certs="/etc/elasticsearch/certs/http_ca.crt",
            ca_certs=self._aqcuire_ssl(),
            basic_auth=(os.environ["ELASTIC-USERNAME"], os.environ["ELASTIC-PASSWORD"])
        )
        logging.info(self.es_client.info())
        atexit.register(self.destroyed)


    def create_index(self, index_name: str, mapping: dict):
        """
        Create an ES index.
        mapping: Mapping of the index
        """
        logging.info(f"Creating index {index_name} with the following schema: {json.dumps(mapping, indent=2)}")
        response = self.es_client.options(ignore_status=400).indices.create(index=index_name, mappings=mapping)
        return response
    
    
    def obliterate_index(self, index_name: str):
        '''
        Obliterate an ES index.
        THIS OPERATION IS IRREVERSABLE
        '''
        logging.info(f"Destroying the index named: {index_name}")
        response = self.es_client.options(ignore_status=400).indices.delete(index=index_name)
        return response


    def index_data(self, index_name: str, data: dict) -> None:
        logging.info(f"Indexing on some data on {index_name}")
        response = self.es_client.index(index=index_name, document=data)
        logging.info(response['result'])
        print(data)

    
    def index_exists(self, index_name: str) -> bool:
        logging.info(f"Checking if {index_name} exists...")
        exists = bool(self.es_client.indices.exists(index=index_name))
        logging.info(
            "It does exist!" if exists else "It does not exist."
        )
        return exists


    def destroyed(self):
        os.remove("http_ca.crt")
        self.es_client.close()

    
    def _aqcuire_ssl(self):
        with open("http_ca.crt", 'w') as f:
            f.write(run(['sudo', 'cat', '/etc/elasticsearch/certs/http_ca.crt'], capture_output=True, text=True).stdout)
        return f"{os.getcwd()}/http_ca.crt"
    