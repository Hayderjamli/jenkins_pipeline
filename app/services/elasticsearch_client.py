from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT")

def get_elasticsearch():
    return Elasticsearch([f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"])
