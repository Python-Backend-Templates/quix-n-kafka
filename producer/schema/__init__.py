import os

from confluent_kafka.schema_registry import SchemaRegistryClient


SCHEMA_REGISTRY_URL = os.environ.get("SCHEMA_REGISTRY_LISTENERS")


client = SchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})


from schema.ping.v1 import Ping
from schema.pong.v1 import Pong
