import requests


class InvalidUrlError(Exception):
    pass


class ParamsNotFoundError(Exception):
    pass


class ShortenerError(Exception):
    pass


def shorten(url=None, params=None, **kwargs):
    """

    Shortens entered url with added parameters (ex api key)

    parameters:

        params = parameters sent to url shortener service
        url = url to shorten

    raises:

        InvalidUrlError | no url entered
        ParamsNotFoundError | no parameters entered
        ShortenerError | Invalid HTTP request or network error

    """
    method = kwargs.get("method", "GET").upper()
    json_body = kwargs.get("json_body")
    json_key = kwargs.get("json_key")
    serviceurl = kwargs.get("serviceurl")
    headers = kwargs.get("headers", {})
    multifile = kwargs.get("multifile", False)
    proxies = kwargs.get("proxies", {})

    if not url or not url.startswith(("http://", "https://")):
        raise InvalidUrlError("No url entered.")
    if not params:
        raise ParamsNotFoundError("No parameters entered.")
    if not serviceurl:
        raise ValueError("No service url provided.")
    try:
        if method == "POST":
            if json_body:
                shortenedurl = requests.post(
                    serviceurl, json=params, headers=headers, proxies=proxies)
            elif multifile:
                files = {}
                for key, value in params.items():
                    files[key] = value
                shortenedurl = requests.post(
                    serviceurl, files=files, headers=headers, proxies=proxies)
            else:
                shortenedurl = requests.post(
                    serviceurl, data=params, headers=headers, proxies=proxies)
        else:
            shortenedurl = requests.get(
                serviceurl, params=params, headers=headers, proxies=proxies)
        shortenedurl.raise_for_status()
        if json_key:
            val = shortenedurl.json().get(json_key, "")
            return val.strip() if isinstance(val, str) else str(val)

        return shortenedurl.text.strip()
    except requests.RequestException as errormessage:
        raise ShortenerError(f"HTTP request failed: {errormessage}")
