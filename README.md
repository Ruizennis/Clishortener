# Clishortener
> A lightweight, feature-rich CLI tool to shorten links using 12+ services—with zero configuration required.

[![PyPI version](https://img.shields.io/pypi/v/Clishortener.svg)](https://pypi.org/project/Clishortener/)

---

## Key Features

* 🚀 **Lightweight & Fast:** Works right out of the terminal.
* 🔌 **12+ Services Pre-configured:** TinyURL, Bitly, Short.io, CleanURI, and more.
* 🛠️ **Custom & Self-Hosted:** Full support for custom domains and YOURLS instances.
* 🎨 **Rich Output:** Optional colorful terminal UI using `rich`.
* ⚡ **Pipeline Friendly:** Pass raw output directly to stdout or other scripts using bare/silent flags.
* 🕹 **Plug & Play** Start shortening immediately after installation, no setup required.

---
## Installation

Install using pip
```bash
pip install clishortener[rich]
```
Or
Install from source using git
```bash
git clone https://github.com/Ruizennis/Clishortener
cd Clishortener
pip install .
```
## Optional Packages
- `rich`

Things Enhanced With rich Installed:
- Available Services menu
- Change default service menu
- Link Output
- Error messages

## Quick Start 🚀
Shorten your first url ✂️
```bash
cshorten https://example.com
```
Set your preferred service as the default 🔧
```bash
# See All Services list for Identifiers!
cshorten -d dagd
```

## All Services 🌐

| Service | Identifier | Requires key |
|---------|---------------|-----------|
| [tinyurl](https://tinyurl.com/) | tinyurl-auth / tinyurl-noauth | Optional |
| [is.gd](https://is.gd/index.php)   | isgd | No | 
| [v.gd](https://v.gd)     | vgd  | No |
| [da.gd](https://da.gd)    | dagd | No |
| [cleanuri](https://cleanuri.com/) | cleanuri | No |
| [ulvis](https://ulvis.net/)   | ulvis | No |
| [short.io](https://short.io) | shortio | Yes |
| [clck.ru](https://clck.ru)   | clckru | No |
| [bit.ly](https://bitly.com)   | bitly | Yes |
| [cutt.ly](https://cutt.ly)  | cuttly | Yes |
| [0x0.st](https://0x0.st/) | 0x0 | No |
| [YOURLS](https://yourls.org/) | yourls | Optional |
| Custom | custom | Optional |

> **Note**: As Of 2026-08-01 The Public 0x0.st Instance Is Temporarily Paused With No ETA For Its Return, Self Hosting is recomended.
> Self-host The Null Pointer (0x0) From https://git.0x0.st/mia/0x0

## Flags 🚩

| Flag | Long Flag | Purpose | Usage |
|------|-----------|---------|---------------|
| -a   | --available | Shows available services | cshorten -a |
| -s   | --service | Allows specifying service for a command | cshorten -s cleanuri https://example.com |
| -d   | --change-default-service | Allows changing the default service | cshorten -d dagd |
| -b   | --bare | Remove rich formatting and write to stdout without formatting | cshorten -b https://example.com >> links.txt |
| -k   | --key | Allows setting an api key for services that require it | cshorten https://example.com/ -s yourls -k KEY -D https://yourls.org |
| -h   | --help | Shows help menu | cshorten -h |
| -S   | --silent | Silences all logging messages | cshorten https://example.com -b -S >> links.txt |
| -D   | --domain | Allows setting a custom domain to connect to (yourls / custom only) | cshorten -s custom -D https://example.com |
| -A   | --auth-parameter | Allows setting auth_param for use with non standard services (YOURLS / custom only) | cshorten -s custom -D https://example.com -A key |
| -U   | --url-parameter | Allows setting url_param for use with non-standard services (YOURLS / custom only) | cshorten -s custom -D https://example.com -A key -U url |
| -H   | --header | Allows setting custom header information for use with header based authentication services (bit.ly, short.io) | cshorten "https://example.com" -s bitly -k "Key" -H "X-Custom-Header: CustomValue"

## Additional Information 📜
- Default URL shortening service is tinyurl (no key / anonymous)
- Identifier is used when specifying a specific link shortening service with -s or -d
- YOURLS is self-hosted only
- Custom & YOURLS allows any URL to be used
- When using Custom or YOURLS use the full URL
- Commands considered "advanced" are uppercase (-A -U -D -S -H)
- `auth_param` is used when determining if a service requires an api key
- `url_param` is what variable is used when sending a request (Default: "url")
- Custom headers should be sent in a key, value format
- --domain allows any URL to be used

## Adding Additional Services 🔨
> Additional Services Can Be Added By Editing `Services.json` And Adding New Entries.

### Anonymous Service Example (**da.gd**)
```json
"dagd": {
        "serviceurl": "https://da.gd/s",
        "method": "GET",
        "params": {
            "url": ""
        }
    }
```
### Authenticated API Example (**short.io**)
```json
"shortio": {
        "serviceurl": "https://api.short.io/links/public",
        "auth_header": "authorization",
        "url_param": "originalURL",
        "method": "POST",
        "json_key": "shortURL",
        "json_body": true,
        "params": {}
}
```

___

## Additional Links & Credits
[Pypi - clishortener](https://pypi.org/project/Clishortener/) 
[Github - Clishorteners](https://github.com/Ruizennis/Clishorteners) 
[Issues - Clishorteners](https://github.com/Ruizennis/Clishorteners/issues)

Credits To Pyshorteners Made By ellisonleao For Inspiring This Tool 
[Pyshorteners](https://github.com/ellisonleao/pyshorteners) 

___

# License
## This project is licensed under the MIT license, see [LICENSE](LICENSE).