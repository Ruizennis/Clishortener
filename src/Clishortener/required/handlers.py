# handlers for subcommands

import sys
import logging
from pathlib import Path
from .rich_print import cli_print
from .shortener import shorten

logger = logging.getLogger(__name__)

try:
    from ..modules.proxy import proxyconfig
    PROXYAVAILABLE = True
except ImportError:
    PROXYAVAILABLE = False
try:
    from rich.console import Console
    from rich.table import Table
    RICHAVAILABLE = True
except ImportError:
    RICHAVAILABLE = False


def loadjson(file: Path) -> dict:
    """Loads json configuration file and returns contents"""
    import json
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        logger.error("Missing keys or malformed json file")
        return {}


def updateuserconf(file: Path, data: dict = None) -> None:
    """Updates user configuration file"""
    import json
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as errormsg:
        logger.error(f"Unable to update configuration file {errormsg}")


def handle_service_default(args, services, userconf):
    if args.default in services:
        userdata = loadjson(userconf) or {}
        if not isinstance(userdata, dict):
            userdata = {}
        userdata["Default-service"] = args.default

        updateuserconf(userconf, userdata)
        if not args.silent:
            cli_print(
                message=(
                    "[bold orange3]New Default Service: "
                    f"[bold cyan]{args.default}"
                ),
                baremessage=f"New Default Service: {args.default}",
                bare=args.bare
            )
        sys.exit(0)
    else:
        logger.error(f'Invalid service "{args.default}"')
        sys.exit(1)


def handle_service_list(args, services):
    cli_print(
        message="[dodger_blue1]• Available Services •",
        baremessage="• Available Services •",
        bare=args.bare
    )
    for key, value in services.items():
        url = value.get('serviceurl', '').replace(
            '{domain}', '[Custom domain]')
        cli_print(
            baremessage=f"{key} • {url}",
            message=f"[bold cyan]{key}[white] • [bold light_green]{url}",
            bare=args.bare
        )
    sys.exit(0)


def handle_security_proxy_edit(args, userconf):
    if not PROXYAVAILABLE:
        logger.error("Proxy Unavailable!")
        sys.exit(1)

    proxies = proxyconfig()
    if proxies:
        userdata = loadjson(userconf) or {}
        userdata["proxies"] = proxies
        updateuserconf(userconf, userdata)
        cli_print(
            message="[bold light_green]Proxy Configuration Saved",
            baremessage="Proxy Configuration Saved",
            bare=args.bare
        )
    sys.exit(0)


def handle_proxy_show(args, userconf):
    userdata = loadjson(userconf) or {}
    proxies = userdata.get("proxies", {})
    if proxies:
        if RICHAVAILABLE:
            if getattr(args, "bare", False):
                for proto, address in proxies.items():
                    print(f"{proto.upper()}={address}")
            else:
                table = Table(title="Current Proxy Settings",
                              show_header=True, header_style="bold cyan")
                table.add_column("Protocol", style="bold white")
                table.add_column("Proxy Address", style="bold light_green")

                for proto, address in proxies.items():
                    table.add_row(proto.upper(), address)

                Console().print(table)
        else:
            cli_print(
                message=(
                    "[bold cyan]Current Proxies: "
                    f"[bold light_green] {proxies}"
                ),
                baremessage=str(proxies),
                bare=getattr(args, "bare", False)
            )
    else:
        cli_print(
            message="[bold orange3]No proxies currently configured.",
            baremessage="No proxies currently configured.",
            bare=getattr(args, "bare", False)
        )
    sys.exit(0)


def handle_proxy_reset(args, userconf):
    userdata = loadjson(userconf) or {}
    if "proxies" in userdata:
        del userdata["proxies"]
        updateuserconf(userconf, userdata)
    cli_print(
        message="[bold light_green]Proxy configuration cleared.",
        baremessage="Proxy configuration cleared.",
        bare=getattr(args, "bare", False)
    )
    sys.exit(0)


def handle_shorten(args, services, fileload):
    if not args.url:
        if not sys.stdin.isatty():
            args.url = sys.stdin.read().strip()
        if not args.url:
            cli_print(
                message=(
                    "[bold orange3]No URL Provided! "
                    "Run cshorten -h For Usage"
                ),
                baremessage="No URL Provided! Run cshorten -h For Usage",
                bare=getattr(args, "bare", False)
            )
            sys.exit(1)

    try:
        servicesconfig = services[args.service].copy()
        if getattr(args, "config", None):
            for item in args.config:
                if "=" in item:
                    key, value = item.split("=", 1)
                    servicesconfig[key.strip()] = value.strip()
                    if value.lower() == "true":
                        servicesconfig[key] = True
                    elif value.lower() == "false":
                        servicesconfig[key] = False
                    else:
                        servicesconfig[key] = value

        serviceurl = servicesconfig["serviceurl"]
        params = servicesconfig["params"].copy()
        urlparam = servicesconfig.get("url_param") or "url"
        params[urlparam] = args.url

        if "{domain}" in serviceurl:
            if not args.domain:
                logger.error(
                    "Using yourls instances requires "
                    "the domain flag to be set as the instances full url"
                )
                sys.exit(1)
            serviceurl = serviceurl.replace(
                "{domain}", args.domain.rstrip("/"))

        auth_keyword = servicesconfig.get("auth_param")
        headers = servicesconfig.get("auth_header")
        headers_dict = {}

        if headers:
            if not args.key:
                logger.error(f"Service {args.service} requires an api key!")
                sys.exit(1)
            api_key = args.key
            if (
                headers.lower() == "authorization"
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

    servicesconfig["serviceurl"] = serviceurl
    servicesconfig["params"] = params
    servicesconfig["headers"] = headers_dict
    servicesconfig["proxies"] = fileload.get("proxies")

    try:
        shortenedurl = shorten(url=args.url, **servicesconfig)
        cli_print(
            message=f"[bold orange3]Shortened url: [bold cyan]{shortenedurl}",
            baremessage=shortenedurl,
            bare=args.bare
        )
    except Exception as errormsg:
        logger.error(f"Unable to shorten {args.url}! Cause: {errormsg}")
