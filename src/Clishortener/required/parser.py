# This file simply holds all the arguments used in main
# and includes an importable helperfunction

import argparse
from .handlers import (
    handle_service_default,
    handle_service_list,
    handle_security_proxy_edit,
    handle_proxy_show,
    handle_proxy_reset,
    handle_keyring_set,
    handle_keyring_clear,
    handle_shorten,
)


class GetParserError(Exception):
    pass


def initurlparser(servicedefault: str) -> argparse.ArgumentParser:
    """Returns arguments related to url shortening"""
    parser = argparse.ArgumentParser(
        usage="cshorten [-h] [-b] [-S] [command] [options]",
        epilog=(
            f"\n Current Default Service: {servicedefault}"
        ),
        description="Run cshorten [command] -h For Help."
    )
    parser._optionals.title = "Options"
    parser._positionals.title = "Positional Arguments"

    # subcommands
    subparsers = parser.add_subparsers(dest="command", metavar="")

    servicecommand = subparsers.add_parser(
        "service",
        help="Manage Shortening Services"
    )
    serviceparser = servicecommand.add_subparsers(
        dest="servicecommand",
        metavar="",
        description="Allows Manageing Services"
    )
    servicecommand.set_defaults(
        func=lambda args, *_: servicecommand.print_help())
    defaultserviceparser = serviceparser.add_parser(
        "default",
        help=(
            "Set Default Service | "
            "USAGE: cshorten "
            "service default <SERVICE>"
        )
    )
    defaultserviceparser.add_argument(
        "default",
        action="store",
        metavar="SERVICE",
        help=(
            f"Changes default service and saves it to"
            f" 'Clishortener_config.json' for future use"
            f" (Current {servicedefault})"
        ),
    )
    defaultserviceparser.set_defaults(func=handle_service_default)
    listparser = serviceparser.add_parser(
        "list",
        help=(
            "List All Available Services"
        )
    )
    listparser.set_defaults(func=handle_service_list)
    securityparser = subparsers.add_parser(
        "security",
        help="Contains Commands Related To Security / OPSEC"
    )
    securitysubparser = securityparser.add_subparsers(
        dest="securitycommand",
        metavar=""
    )
    securityparser.set_defaults(
        func=lambda args, *_: securityparser.print_help()
    )
    proxyparser = securitysubparser.add_parser(
        "proxy",
        help="Interactively Edit HTTP/HTTPS Proxy Configurations"
    )
    proxyparser.set_defaults(func=lambda args, *_: proxyparser.print_help())
    proxysubparsers = proxyparser.add_subparsers(
        dest="proxycommand", metavar="")
    proxyedit = proxysubparsers.add_parser(
        'edit',
        help="Edit Proxy Configurations"
    )
    proxyedit.set_defaults(func=handle_security_proxy_edit)
    proxyshow = proxysubparsers.add_parser(
        'show',
        help="Display Current Proxy Configurations"
    )
    proxyshow.set_defaults(func=handle_proxy_show)
    proxyreset = proxysubparsers.add_parser(
        'reset',
        help="Clear Saved Proxy Configurations"
    )
    proxyreset.set_defaults(func=handle_proxy_reset)
    shortenparser = subparsers.add_parser(
        "shorten",
        help="Shortens URLS"
    )
    shortenparser.add_argument(
        "url",
        action="store",
        nargs="?",
        default=None,
        help="Url that is shortened."
    )
    advanced = shortenparser.add_argument_group("Advanced Commands")

    shortenparser.add_argument(
        "-s",
        "--service",
        default=servicedefault,
        action="store",
        help="Urlshortening service to use",
    )
    shortenparser.add_argument(
        "--no-strip",
        action="store_true",
        help="Disable automatic tracking parameter stripping"
    )
    shortenparser.add_argument(
        "-k",
        "--key",
        action="store",
        help="Allows adding an api key for services that require it",
    )
    keyringparser = securitysubparser.add_parser(
        "keys",
        help=(
            'Set or Reset api keys, '
            'keys are autochecked when shortening '
            'using an authenticated service'
        )
    )
    keyringsubparser = keyringparser.add_subparsers(
        dest="keyringcommand",
        metavar=""
    )
    keyringset = keyringsubparser.add_parser(
        "set",
        help="Set a service API key."
    )
    keyringset.add_argument(
        "service",
        help="Service that the key is set for."
    )
    keyringset.set_defaults(func=handle_keyring_set)
    keyringclear = keyringsubparser.add_parser(
        "clear",
        help=(
            "Clear all set API keys, "
            "accepts specifying a service identifier to only "
            "clear that services key."
        )
    )
    keyringclear.add_argument(
        "service",
        nargs="?",
        default=None,
        help="Optionally add service identifier to reset a specific key only."
    )
    keyringclear.set_defaults(func=handle_keyring_clear)
    keyringclear.set_defaults(func=handle_keyring_clear)
    parser.add_argument(
        "-b",
        "--bare",
        action="store_true",
        help="Ensures command only returns url and removes rich coloring"
    )
    parser.add_argument(
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
        '-c',
        '--config',
        action='append',
        help=(
            'Allows setting temporary overrides '
            'for services.json key: value pairs.'
        )
    )
    shortenparser.set_defaults(func=handle_shorten)

    return parser
