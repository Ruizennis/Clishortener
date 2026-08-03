# Contains An Helper function for rich and configures logger
import logging
import os
from sys import stdout
RICHLOADED = True
NONELIST = ['', None, 'None']
NO_COLOR = False if os.environ.get('NO_COLOR') in NONELIST else True
FORCE_COLOR = os.environ.get("FORCE_COLOR", "").lower() in ("1", "true")


class PrintError(Exception):
    pass


try:
    import rich
    from rich.logging import RichHandler
    logging.basicConfig(
        level=logging.WARN,
        format="%(message)s",
        handlers=[RichHandler(
            rich_tracebacks=False,
            log_time_format="[%H:%M:%S]",
            show_path=False, markup=True
        )]
    )
    RICHLOADED = True
except ImportError:
    bare = True
    RICHLOADED = False
    logging.basicConfig(
        level=logging.WARN,
        format="%(message)s"
    )


def cli_print(message: str, baremessage: str, bare: bool = False) -> str:
    if (not stdout.isatty() and not FORCE_COLOR) or not RICHLOADED or NO_COLOR:
        bare = True
    if not message or not baremessage:
        raise PrintError("Print Requires 2 Arguments, message and baremessage")
    if bare:
        stdout.write(baremessage + "\n")
    else:
        rich.print(message)
