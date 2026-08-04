# PYTHON_ARGCOMPLETE_OK
import sys
import json
import logging
from pathlib import Path
from .required.parser import initurlparser
logger = logging.getLogger(__name__)
bare = False

try:
    import argcomplete
    ARGCOMPLETEAVAILABLE = True
except ImportError:
    ARGCOMPLETEAVAILABLE = False


def configpath() -> Path:
    home = Path.home() / ".config" / "clishortener" / "usr"
    home.mkdir(parents=True, exist_ok=True)
    return home / "usrconfig.json"


def loadjson(file: Path) -> dict:
    """Loads json configuration file and returns contents"""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        logger.error("Missing keys or malformed json file")


def updateuserconf(file: Path, data: dict = None) -> None:
    """Updates user configuration file to update default service provider"""
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as errormsg:
        logger.error(f"Unable to update configuration file {errormsg}")


def main():
    servicedefault = "tinyurl-noauth"
    initlocation = Path(__file__).resolve().parent / "usr"
    userconf = configpath()
    try:
        fileload = loadjson(userconf) or {}
        if not isinstance(fileload, dict):
            fileload = {}
        servicedefault = fileload.get("Default-service", servicedefault)
    except FileNotFoundError:
        pass

    servicepath = initlocation / "services.json"
    services = loadjson(servicepath)
    parser = initurlparser(servicedefault)
    if ARGCOMPLETEAVAILABLE:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.silent:
        logging.disable(logging.CRITICAL)
    if not args.command:
        parser.print_help()
        sys.exit(0)
    if hasattr(args, "func"):
        if args.command == "service":
            if args.servicecommand == "default":
                args.func(args, services, userconf)
            elif args.servicecommand == "list":
                args.func(args, services)
            else:
                args.func(args)
        elif args.command == "security":
            if args.securitycommand == "proxy":
                args.func(args, userconf)
            elif args.securitycommand == "keys":
                args.func(args, services)
            else:
                args.func(args)
        elif args.command == "shorten":
            args.func(args, services, fileload)
        else:
            args.func(args)


if __name__ == "__main__":
    main()
