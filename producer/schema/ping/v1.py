from dataclasses import dataclass


@dataclass
class Ping:
    message: str
    message_to_delete: str
    timestamp: int
