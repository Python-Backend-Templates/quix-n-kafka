import argparse
from abc import ABC, abstractmethod
from typing import List


class CLI(ABC):
    parser: argparse.ArgumentParser
    name: str

    @abstractmethod
    def run(self, args: List[str]) -> None: ...
