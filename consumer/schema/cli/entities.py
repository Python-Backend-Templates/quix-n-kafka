import argparse
from dataclasses import dataclass
from typing import List, Any, Sequence


@dataclass
class CLIArgument:
    flags: Sequence[str]
    help: str = ""
    default: Any = None
    const: Any = None
    nargs: str | None = None
    choices: List[str] | None = None
    action: type[argparse.Action] | None = None
