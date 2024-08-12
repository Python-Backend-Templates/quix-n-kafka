import argparse
import sys
import os
from typing import Tuple, List

from schema import utils
from schema.cli import config
from schema.cli.interfaces import CLI
from schema.cli.entities import CLIArgument


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class SchemaRegistryCLI(CLI):
    def __init__(
        self,
        name: str,
        parser: argparse.ArgumentParser,
        arguments: Tuple[CLIArgument],
        owidth: int | None = None,  # output width
    ):
        self.name = name
        self.parser = parser
        self.arguments = arguments
        self.owidth = owidth

        self._init_arguments()

    def _init_arguments(self) -> None:
        for argument in self.arguments:
            kwargs = {
                "help": argument.help,
                "default": argument.default,
                "const": argument.const,
                "nargs": argument.nargs,
                "choices": argument.choices,
                "action": argument.action,
            }
            self.parser.add_argument(
                *argument.flags, **{k: v for k, v in kwargs.items() if v is not None}
            )

    def run(self, args: List[str]) -> None:
        self._validate_args(args)
        namespace = self.parser.parse_args(args)
        if not namespace.schema:
            self._show_error("Schema is required.")
            exit(1)
        print(namespace)
        match namespace.action:
            case "register":
                if not namespace.filepath:
                    self._show_error("Filepath is required for schema registration.")
                    exit(1)
                self._register_schema(namespace)
            case "list":
                self._list_schemas(namespace)
            case "latest":
                self._latest_schema(namespace)
            case "info":
                if not namespace.version:
                    self._show_error("Version is required for schema info.")
                    exit(1)
                self._schema_info(namespace)
            case "set_comp":
                if not namespace.compability:
                    self._show_error(
                        "Compability is required for setting schema compability."
                    )
                    exit(1)
                self._set_comp(namespace)
            case "get_comp":
                self._get_comp(namespace)
            case "test_comp":
                if not namespace.compability:
                    self._show_error(
                        "Compability is required for testing schema compability."
                    )
                    exit(1)
                if not namespace.version:
                    self._show_error(
                        "Version is required for testing schema compability."
                    )
                    exit(1)
                self._test_comp(namespace)
            case "delete_version":
                if not namespace.version:
                    self._show_error("Version is required for version deleting.")
                    exit(1)
                self._delete_version(namespace)
            case "soft_delete_schema":
                self._soft_delete_schema(namespace)
            case "hard_delete_schema":
                self._hard_delete_schema(namespace)
            case _:
                self.parser.print_help()
        sys.exit(0)

    def _validate_args(self, args: List[str]) -> None:
        if len(args) == 0:
            self.parser.print_help()
            sys.exit(0)

    def _show(self, *texts: str, is_error: bool = False) -> None:
        width = self.owidth or (self._get_terminal_witdh() // 2)
        print(color.BOLD, color.RED if is_error else color.DARKCYAN)
        print("-" * width)
        print(*[text.center(width) for text in texts], sep="\n")
        print("-" * width)
        print(color.GREEN, config.CLI_GRATITUDE)
        print(color.END)

    def _show_error(self, error: str) -> None:
        self._show(
            "There was an error while handling a dns query.",
            f'Error message: "{error}"',
            is_error=True,
        )

    def _get_terminal_witdh(self) -> int:
        return os.get_terminal_size().columns

    def _register_schema(self, namespace) -> None:
        try:
            utils.register_json_schema(
                filepath=namespace.filepath,
                schema_name=namespace.schema,
            )
        except Exception as e:
            self._show_error(str(e))
        else:
            self._show("Schema registered successfully")

    def _list_schemas(self, namespace) -> None:
        try:
            schemas = utils.get_versions(schema_name=namespace.schema)
            self._show(*(str(schema) for schema in schemas))
        except Exception as e:
            self._show_error(str(e))

    def _latest_schema(self, namespace) -> None:
        try:
            schema = utils.get_latest_version(schema_name=namespace.schema)
            self._show(
                f"ID: {schema.schema_id}\n"
                f"SUBJECT: {schema.subject}\n"
                f"VERSION: {schema.version}\n"
                f"SCHEMA_TYPE: {schema.schema.schema_type}\n"
                f"SCHEMA_STR: {schema.schema.schema_str}\n"
            )
        except Exception as e:
            self._show_error(str(e))

    def _schema_info(self, namespace) -> None:
        try:
            schema = utils.get_version(
                schema_name=namespace.schema, version=namespace.version
            )
            self._show(
                f"ID: {schema.schema_id}\n"
                f"SUBJECT: {schema.subject}\n"
                f"VERSION: {schema.version}\n"
                f"SCHEMA_TYPE: {schema.schema.schema_type}\n"
                f"SCHEMA_STR: {schema.schema.schema_str}\n"
            )
        except Exception as e:
            self._show_error(str(e))

    def _set_comp(self, namespace) -> None:
        try:
            compability = utils.set_compability(namespace.schema, namespace.compability)
            self._show(f"Schema compability successfully set to {compability}")
        except Exception as e:
            self._show_error(str(e))

    def _get_comp(self, namespace) -> None:
        try:
            compability = utils.get_compability(namespace.schema)
            self._show(f"Schema compability is {compability}")
        except Exception as e:
            self._show_error(str(e))

    def _test_comp(self, namespace) -> None:
        try:
            success = utils.get_compability(namespace.schema)
            if success:
                self._show(f"Schema compability test succeeded.")
            else:
                self._show_error(f"Schema compability test failed.")
        except Exception as e:
            self._show_error(str(e))

    def _delete_version(self, namespace) -> None:
        try:
            version = utils.delete_version(namespace.schema, namespace.version)
            self._show(f"Version {version} is deleted.")
        except Exception as e:
            self._show_error(str(e))

    def _soft_delete_schema(self, namespace) -> None:
        try:
            versions = utils.delete_schema(namespace.schema, permanent=False)
            self._show(f"Schema soft-deleted with versions: {versions}.")
        except Exception as e:
            self._show_error(str(e))

    def _hard_delete_schema(self, namespace) -> None:
        try:
            versions = utils.delete_schema(namespace.schema, permanent=True)
            self._show(f"Schema hard-deleted with versions: {versions}.")
        except Exception as e:
            self._show_error(str(e))
