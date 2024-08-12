import sys
from typing import List


def main(args: List[str]):
    from schema.cli.di import Container

    container = Container()
    container.cli().run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
