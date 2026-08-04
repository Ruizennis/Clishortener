# Clishortener
> A lightweight, feature-rich CLI tool to shorten links using 12+ services—with zero configuration required.


[![PyPI version](https://img.shields.io/pypi/v/Clishortener.svg)](https://pypi.org/project/Clishortener/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![PyPI version](https://img.shields.io/pypi/v/Clishortener.svg?color=blue)](https://pypi.org/project/Clishortener/)
[![PyPI Total Downloads](https://img.shields.io/pepy/dt/Clishortener.svg)](https://pepy.tech/project/Clishortener)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Tested for Termux](https://img.shields.io/badge/Tested_for-Termux-17020Fstyle=flat&logo=termux&logoColor=white&color=000000)


![Asciinema Showcase](https://raw.githubusercontent.com/Ruizennis/Clishortener/main/Assets/demo.gif)


## Key Features 

* 🔌 **12+ Services:** TinyURL, Bitly, Short.io, CleanURI, and more.
* 🛠️ **Custom & Self-Hosted:** Full support for custom domains and YOURLS instances.
* 🎨 **Colored Output:** Optional colorful terminal UI using `rich`.
* 🛡️ **Privacy Focused:** Automatically strips common tracking urls.
* ⚡ **Pipeline Friendly:** Pass raw output directly to stdout or other scripts using bare/silent flags.
* 🕹 **Plug & Play:** Start shortening immediately after installation, no setup required.

---

## Installation Options 📥

### Via PyPI (recommended)
```bash
pip install clishortener[rich]
```
> This will also install rich. To install necessary files only, use `pip install clishortener`

### From source via git
```bash
git clone https://github.com/Ruizennis/Clishortener
cd Clishortener
pip install .
```

### Installing all optional packages
```bash
pip install clishortener[full]
activate-global-python-argcomplete # This will setup argcomplete globally
```

---

## Quick Start
Shorten your first url ✂️
```bash
cshorten shorten https://example.com
```
Set your preferred service as the default 🔧
```bash
cshorten service default <servicename>
```
List all available services 📜
```bash
cshorten service list
```
Pipe data to create a pipeline 🔗
```bash
echo "https://example.com" | cshorten shorten >> links.txt
```

> [!IMPORTANT]
> The Default Shortening Service Is Tinyurl (No Api Key Is Required)

---

## Supported Services 🌐

| Service | Identifier | API Key Required? |
| :--- | :--- | :--- |
| **TinyURL** | `tinyurl-noauth` / `tinyurl-auth` | Optional |
| **is.gd** / **v.gd** | `isgd` / `vgd` | No |
| **da.gd** | `dagd` | No |
| **clck.ru** | `clckru` | No |
| **ulvis.net** | `ulvis` | No |
| **CleanURI** | `cleanuri` | No |
| **Bitly** | `bitly` | **Yes** |
| **Cuttly** | `cuttly` | **Yes** |
| **Short.io** | `shortio` | **Yes** |
| **Rebrandly** | `rebrandly` | **Yes** |
| **YOURLS** | `yourls` | Optional |
| **Custom Service** | `custom` | Depends on service chosen |

> [!IMPORTANT]  
> **Privacy & Service Usage:** Requests routed through third-party shorteners are subject to each provider's independent privacy and logging practices. Self-hosted options (`YOURLS`, `custom`) give you total control over data logging.


<details>
<summary><b>📜 View Provider Terms & Privacy Policies</b></summary>

<br>

| Provider | Legal & Policy Links |
| :--- | :--- |
| **TinyURL** | [Privacy Policy](https://tinyurl.com/app/privacy-policy) · [Terms of Service](https://tinyurl.com/app/terms-of-service) |
| **is.gd** | [Terms & Privacy Policy](https://is.gd/terms.php) |
| **v.gd** | [Terms & Privacy Policy](https://v.gd/terms.php) |
| **da.gd** | [Source & Licensing](https://github.com/dagd/dagd) |
| **clck.ru** | [Privacy Policy](https://yandex.com/legal/confidential/) · [Terms of Use](https://yandex.ru/legal/clck_termsofuse/) |
| **ulvis.net** | [Service Terms](https://ulvis.net/) |
| **CleanURI** | [Privacy Policy](https://cleanuri.com/privacy) · [Terms of Service](https://cleanuri.com/terms) |
| **Bitly** | [Privacy Policy](https://bitly.com/pages/privacy) · [Terms of Service](https://bitly.com/pages/terms-of-service) |
| **Cuttly** | [Privacy Policy](https://cutt.ly/privacy-policy) · [Terms of Service](https://cutt.ly/terms-of-service) |
| **Short.io** | [Privacy Policy](https://short.io/privacy) · [Terms of Service](https://short.io/terms) |
| **Rebrandly** | [Privacy Policy](https://rebrandly.com/privacy-policy) · [Terms & Conditions](https://rebrandly.com/terms-and-conditions) |

 **Disclaimer:** These legal policy links are provided for convenience only, links may change over time and as a solo developer, I can't guarantee every link stays up to date.

</details>

---

## Requirements 📦

| Package | Type | Purpose |
| :--- | :--- | :--- |
| `requests` | **Required** | Handles HTTP calls to shortening APIs |
| `PySocks`  | Optional | Allows more types of proxying (SOCKS) |
| `rich` | Optional | Adds terminal colors, menus, and visual styling |
| `argcomplete` | Optional | Provides shell auto-completion for `cshorten` |
| `keyring` / `keyrings.alt` | Optional | Allows saving API keys securely for automatic authentication |

> [!NOTE]
> If you are using Termux or a terminal that doesn't support keyring use keyrings.alt instead. (`pip install keyrings.alt`)

---

## Global Flags

| Flag | Long Flag | Purpose |
|------|-----------|---------|
| -b   | --bare | Remove rich formatting and write to stdout without formatting |
| -h   | --help | Shows help menu |
| -S   | --silent | Silences all logging messages |

## Shortening Flags 

| Flag | Long Flag | Purpose |
|------|-----------|---------|
| -s   | --service | Allows specifying service for a command |
| -k   | --key     | Allows setting an api key for services that require it |
|      | --no-strip| Disables automatic tracker parameter removal |

## Additional Commands >_

| Category | Command | Description | Usage Example |
| :--- | :--- | :--- | :--- |
| **Service** | `default` | Set default shortening service | `cshorten service default <service>` |
| **Service**| `list` | List all available services | `cshorten service list` |
| **Security** | `proxy edit` | Edit proxy configuration | `cshorten security proxy edit` |
| **Security** | `proxy show` | Show current proxy configuration | `cshorten security proxy show` |
| **Security** | `proxy reset` | Remove proxy configuration | `cshorten security proxy reset` |
| **Security** | `keys set` | Add an api key for a service | `cshorten security keys set bitly`|
| **Security** | `keys clear` | Clears ALL set api keys or just for specified service | `cshorten security keys clear bitly`|

---

## Notes & Usage Tips 💡

* **Self-Hosted & Custom Domains:** Use the full URL and set the `--domain` flag when using `yourls` or `custom` providers.
* **API Keys:** API keys can be provided via the `-k` / `--key` flag for services requiring authentication.
* **Service Identifiers:** When specifying or setting a default service, always use the service's Identifier (e.g., dagd, tinyurl-auth) rather than its display name or URL.

<details>
<summary><b>⚙️ Advanced Configuration</b></summary>

> - **Custom / YOURLS:** Requires full URL endpoint and the `--domain` flag.
> - **Custom Headers:** Sent in `key: value` format.
> - **Config Parameters:** `auth_param` specifies key requirements; `url_param` sets the request payload variable (defaults to `"url"`).
> - **NO COLOR:** We proudly support the NO_COLOR initiative. Add NO_COLOR=1 to os.environ to disable output styling
> - **FORCE_COLOR:** Add FORCE_COLOR=1 to your env variables to force color for use in asciinema or vhs recordings.
> - **Pipes:** We support piping data, when piping bare is automatically appiled ensuring no color and only url is sent allowing for more complex pipelines.
> - **Advanced Proxy Networks:** SOCKS proxies and TOR routing is fully supported if you install the required add-on for requests, simply add your socks proxy URL to the proxy list.

> [!WARNING]
> Using SOCKS proxies requires pysocks, install PySocks with `pip install "requests[socks]"`

</details>

---

<details>
<summary><b>Adding Additional Services Examples 🔨</b></summary>

> [!IMPORTANT]
> Additional services can be added By editing `services.json` (/.config/clishortener/usr/usrconfig.json) and adding new entries.

> [!NOTE]
> Httpbin is not a legitimate URL shortening service and is instead intended for development purposes. (e.g seeing public IP address to confirm requests are proxied.)

### Adding httpbin as a service example
```json
"httpbin": {
    "serviceurl": "https://httpbin.org/post",
    "method": "POST",
    "auth_header": "apikey",
    "url_param": "destination",
    "params": {
        "destination": ""
    }
}
```

#### Testing httpbin example
```bash
cshorten shorten https://example.com -s httpbin -k ApiKey
```

### No Key Service JSON Example 🔓

```json
"0x0": {
        "serviceurl": "https://0x0.st",
        "method": "POST",
        "multifile": true,
        "url_param": "shorten",
        "json_body": false,
        "params": {}
     },
```
#### Testing 0x0 example
```bash
cshorten shorten https://example.com -s 0x0
```
> [!WARNING]
> As of 2026-08-01 file hosting on the public [0x0.st](0x0.st) instance is temporarily paused with no ETA for its return, self hosting is recommended.
> Self-host The Null Pointer (0x0) from [The Official Git Repository](https://git.0x0.st/mia/0x0).

### Authenticated API JSON Example 🔐

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

</details>

---

## Planned Features 📌
- [X] Saving api keys with Keyring & automatically loading saved api keys 
- [ ] Saving links created to a file (Off by default)

---

## Additional Links & Credits 🔗
- [PyPI - Clishortener](https://pypi.org/project/Clishortener/)  
- [Github - Clishortener](https://github.com/Ruizennis/Clishortener)  
- [Issues - Clishortener](https://github.com/Ruizennis/Clishortener/issues)  
- [The No Color Initiative](https://no-color.org/)  

Credits to [Pyshorteners](https://github.com/ellisonleao/pyshorteners)  made by ellisonleao for inspiring this tool  

---

## License
**This project is licensed under the MIT license, see [LICENSE](LICENSE).**
