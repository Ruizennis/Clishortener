import sys
import json
import logging
import argparse
from pathlib import Path
from sys import stdout
from .Shortener import shorten
from rich.logging import RichHandler

bare = False
try:
    from rich import print
except ImportError:
    bare = True
logging.basicConfig(
    level=logging.WARN,
    format="%(message)s",
    handlers=[RichHandler(
        rich_tracebacks=False,
        log_time_format="[%H:%M:%S]",
        show_path=False, markup=True
    )]
)
logger = logging.getLogger(__name__)


def configpath() -> Path:
    home = Path.home() / ".config" / "clishortener"
    home.mkdir(parents=True, exist_ok=True)
    return home / "Clishortener_config.json"


def loadjson(file: Path) -> dict:
    """Loads json configuration file and returns contents"""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        logger.error("Missing keys or malformed json file")


def updatedefaultservice(file: Path, servicedefault: str) -> None:
    """Updates user configuration file to update default service provider"""
    try:
        with open(file, "w") as f:
            json.dump({"Default-service": servicedefault}, f, indent=4)
    except Exception as errormsg:
        logger.error(f"Unable to update configuration file {errormsg}")


def writeurl(url: str, write_bare: bool = bare or False):
    if not sys.stdout.isatty():
        if write_bare or bare:
            stdout.write(url)
        else:
            stdout.write(f"Shortened url: {url}")
    else:
        if write_bare or bare:
            print(url)
        else:
            print(f"[bold orange3]Shortened url: [bold cyan]{url}")


def initparser(servicedefault: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser._optionals.title = "Options"
    parser._positionals.title = "Positional arguments"
    advanced = parser.add_argument_group("Advanced Commands")
    miscellaneous = parser.add_argument_group("Miscellaneous Commands")
    parser.add_argument(
        "url",
        action="store",
        nargs="?",
        default=None,
        help="Url that is shortened."
    )
    parser.add_argument(
        "-s",
        "--service",
        default=servicedefault,
        action="store",
        help="Urlshortening service to use",
    )
    miscellaneous.add_argument(
        "-a",
        "--available",
        action="store_true",
        help="Show available services"
    )
    parser.add_argument(
        "-k",
        "--key",
        action="store",
        help="Allows adding an api key for services that require it",
    )
    parser.add_argument(
        "-b",
        "--bare",
        action="store_true",
        help="Ensures command only returns url"
    )
    advanced.add_argument(
        "-S",
        "--silent",
        action="store_true",
        help="Silences all error messages"
    )
    advanced.add_argument(
        "-D",
        "--domain",
        action="store",
        help="Allows setting a domain for yourls instances",
    )
    advanced.add_argument(
        "-A",
        "--auth-parameter",
        action="store",
        help=(
            "Allows setting custom auth_param "
            "for use with selfhosted "
            "or non standard services"
        ),
    )
    advanced.add_argument(
        "-H",
        "--header",
        action="append",
        help=(
            "Allows setting custom headers "
            "for services that use POST (bitly, shortio)"
        ),
    )
    advanced.add_argument(
        "-U",
        "--url-parameter",
        action="store",
        help=(
            "Allows setting the url_param variable "
            "which is used for finding proper url key for a service"
        ),
    )
    miscellaneous.add_argument(
        "-d",
        "--change-default-service",
        action="store",
        metavar="SERVICE",
        help=(
            f"Changes default service and saves it to"
            f" 'Clishortener_config.json' for future use"
            f" (Current {servicedefault})"
        ),
    )
    return parser.parse_args()


def main():
    servicedefault = "tinyurl-noauth"
    initlocation = Path(__file__).resolve().parent
    userconf = configpath()
    try:
        fileload = loadjson(userconf)
        servicedefault = fileload["Default-service"] or servicedefault
    except FileNotFoundError:
        pass
    args = initparser(servicedefault)

    servicepath = initlocation / "Services.json"
    services = loadjson(servicepath)

    if args.silent:
        logging.disable(logging.CRITICAL)
    if args.change_default_service:
        if args.change_default_service in services:
            updatedefaultservice(userconf, args.change_default_service)
            if not args.silent:
                if args.bare:
                    sys.stdout.write(
                        f"New Default service: {args.change_default_service}\n"
                    )
                else:
                    print(
                        f"[bold orange3]New Default service: "
                        f"[bold cyan]{args.change_default_service}"
                    )
            sys.exit(0)
        else:
            logger.error(f'Invalid service "{args.change_default_service}"')
            sys.exit(1)

    if args.available:
        if args.bare:
            print("• Available Services •")
            for key, value in services.items():
                print(
                    f"{key} • "
                    f"{value.get('serviceurl')}"
                    ".replace('{domain}', '[Custom domain]')"
                )
            sys.exit(0)
        else:
            print("[bold green]• Available Services •")
            for key, value in services.items():
                print(
                    f"[bold cyan]{key}"
                    "[white]• [bold light_green]"
                    "{value.get('serviceurl')"
                    ".replace('{domain}', '[Custom domain]')}"
                )
            sys.exit(0)
    if not args.url and args.bare:
        sys.stdout.write(
            "No url provided!"
            "Usage: cshorten <url> [Optional flags]"
        )
        sys.exit(1)
    elif not args.url:
        print(
            "[bold orange3]"
            "No url provided!"
            "Usage: cshorten <url> [Optional flags]"
        )
        sys.exit(1)
    try:
        servicesconfig = services[args.service].copy()
        serviceurl = servicesconfig["serviceurl"]
        params = servicesconfig["params"].copy()
        urlparam = args.url_parameter or servicesconfig.get(
            "url_param") or "url"
        params[urlparam] = args.url
        if "{domain}" in serviceurl:
            if not args.domain:
                logger.error(
                    "Using yourls instances requires the domain flag"
                    " to be set and a valid yourls instance at domain"
                )
                sys.exit(1)
            domain = args.domain.rstrip("/")
            serviceurl = serviceurl.replace("{domain}", domain)
        auth_keyword = args.auth_parameter or servicesconfig.get("auth_param")

        headers_dict = {}
        if args.header:
            for raw in args.header:
                if ":" in raw:
                    key, value = raw.split(":", 1)
                    headers_dict[key.strip()] = value.strip()
        headers = servicesconfig.get("auth_header")

        if headers:
            if not args.key:
                logger.error(f"Service {args.service} requires an api key!")
                sys.exit(1)
            api_key = args.key
            if (
                headers
                and headers.lower() == "authorization"
                and not api_key.startswith("Bearer ")
            ):
                api_key = f"Bearer {api_key}"
            headers_dict[headers] = api_key
        elif auth_keyword:
            if not args.key:
                logger.error(f"Service {args.service} requires an api key!")
                sys.exit(1)
            params[auth_keyword] = args.key
    except KeyError as e:
        logger.error(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as errormsg:
        logger.critical(f"An unexpected error occurred! {errormsg}")
        sys.exit(1)
    servicesconfig["serviceurl"] = serviceurl
    servicesconfig["params"] = params
    servicesconfig["headers"] = headers_dict
    try:
        shortenedurl = shorten(url=args.url, **servicesconfig)
        writeurl(shortenedurl, write_bare=args.bare)
    except Exception as errormsg:
        logger.error(f"Unable to shorten {args.url}! Cause: {errormsg}")


if __name__ == "__main__":
    main()
