import json
import logging
import os

from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()
endpoint = os.environ["MODELHUB_COSMOS_ENDPOINT"]
credential = os.environ["MODELHUB_COSMOS_KEY"]


class CosmosDBAccessPoint:
    def __init__(self):
        DATABASE_NAME = "serverlessdb"
        CONTAINER_NAME = "data-readings"
        logging.info("Connecting to CosmosDB")
        self.client = CosmosClient(url=endpoint, credential=credential)
        logging.info("Retrieving database and container")
        self.database = self.client.create_database_if_not_exists(id=DATABASE_NAME)
        key_path = PartitionKey(path="/segment_id")
        self.container = self.database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=key_path,
        )
        logging.info("Connected to CosmosDB!")

    def query_all(self):
        logging.info("Querying all data from CosmosDB")
        print("Querying all data from CosmosDB")
        results = self.container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True,
        )
        items = [item for item in results]
        print("Query complete")
        return json.dumps(items, indent=True)
