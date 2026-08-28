from sys import stdout
try:
    from Clishortener.required.rich_print import cli_print
except ImportError:
    from ..required.rich_print import cli_print

try:
    import qrcode
    QRAVAILABLE = True
except ImportError:
    QRAVAILABLE = False


def getqr(args: dict, url: str):
    if not QRAVAILABLE:
        cli_print(
            message="[bold red]Qr Code Unavailable!",
            baremessage="Qr Code Unavailable",
            bare=getattr(args, "bare", False),
        )
        return
    qr = qrcode.QRCode()
    qr.add_data(str(url))
    qr.print_ascii(out=stdout)
