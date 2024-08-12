from schema.cli.entities import CLIArgument
from schema.utils import COMPABILITY_TYPE_TUPLE


CLI_GREETING = """
Welcome to Confluent Schema Registry CLI!
"""
CLI_GRATITUDE = """
Thank you for using Confluent Schema Registry CLI!
"""


CLI_DESCRIPTION = "Schema Registry CLI"
CLI_ARGUMENTS = (
    CLIArgument(
        flags=("action",),
        help="Action",
        choices=[
            "register",
            "list",
            "latest",
            "info",
            "set_comp",
            "get_comp",
            "test_comp",
            "delete_version",
            "soft_delete_schema",
            "hard_delete_schema",
        ],
    ),
    CLIArgument(
        flags=("-f", "--filepath"),
        help="Filepath to schema definition.",
        nargs="?",
    ),
    CLIArgument(flags=("-s", "--schema"), help="Schema name."),
    CLIArgument(flags=("-v", "--version"), help="Schema version."),
    CLIArgument(
        flags=("-c", "--compability"),
        help="Schema compability.",
        choices=COMPABILITY_TYPE_TUPLE,
    ),
)
CLI_OWIDTH = 97  # output width
