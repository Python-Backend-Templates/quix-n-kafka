from argparse import ArgumentParser, RawDescriptionHelpFormatter

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from schema.cli import config
from schema.cli.app import SchemaRegistryCLI, color


class Container(DeclarativeContainer):
    parser = providers.Singleton(
        ArgumentParser,
        description=color.GREEN + config.CLI_GREETING + color.END,
        formatter_class=RawDescriptionHelpFormatter,
    )
    cli = providers.Singleton(
        SchemaRegistryCLI,
        name="sr",
        parser=parser,
        arguments=config.CLI_ARGUMENTS,
        owidth=config.CLI_OWIDTH,
    )
