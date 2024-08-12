import json
from typing import List, Literal

from confluent_kafka.schema_registry import (
    Schema,
    RegisteredSchema,
)

from schema import client


COMPABILITY_TYPE = Literal[
    "BACKWARD",
    "BACKWARD_TRANSITIVE",
    "FORWARD",
    "FORWARD_TRANSITIVE",
    "FULL",
    "FULL_TRANSITIVE",
    "NONE",
]
COMPABILITY_TYPE_TUPLE = [
    "BACKWARD",
    "BACKWARD_TRANSITIVE",
    "FORWARD",
    "FORWARD_TRANSITIVE",
    "FULL",
    "FULL_TRANSITIVE",
    "NONE",
]


def register_json_schema(filepath: str, schema_name: str) -> None:
    with open(filepath, "r") as file:
        client.register_schema(
            subject_name=schema_name,
            schema=Schema(
                schema_str=json.dumps(json.load(file)),
                schema_type="JSON",
            ),
        )


def get_latest_version(schema_name: str) -> RegisteredSchema:
    return client.get_latest_version(schema_name)


def get_versions(schema_name: str) -> List[int]:
    return client.get_versions(schema_name)


def get_version(schema_name: str, version: str) -> RegisteredSchema:
    return client.get_version(schema_name, version)


def get_compability(schema_name: str) -> str:
    return client.get_compatibility(schema_name)


def set_compability(schema_name: str, compatibility: COMPABILITY_TYPE) -> str:
    return client.set_compatibility(schema_name, compatibility)


def test_compability(
    schema_name: str, compatibility: COMPABILITY_TYPE, version: str
) -> bool:
    return client.test_compatibility(schema_name, compatibility, version)


def delete_schema(schema_name: str, permanent: bool) -> List[int]:
    return client.delete_subject(schema_name, permanent=permanent)


def delete_version(schema_name: str, version: str) -> int:
    return client.delete_version(schema_name, version)
