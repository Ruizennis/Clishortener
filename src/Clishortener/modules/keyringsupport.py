import sys
from ..required.rich_print import cli_print

PKGNAME = "clishortener"
KEYRING = False
KEYRINGALT = False
try:
    import keyring

    KEYRING = True
except ImportError:
    pass

isbare = any(arg in sys.argv for arg in ("-b", "--bare"))
try:
    if not KEYRING:
        try:
            import keyrings.alt.file

            KEYRINGALT = True
        except ImportError:
            cli_print(
                message=(
                    "[bold red]Keyring Unavailable, " "Both backends failed to import!"
                ),
                baremessage=("Keyring Unavailable, Both" " backends failed to import!"),
                bare=isbare,
            )
except ImportError:
    pass


def setkey(servicename, key):
    if KEYRINGALT:
        backend = keyrings.alt.file.EncryptedKeyring()
        keyring.set_keyring(backend)
    return keyring.set_password(PKGNAME, servicename, key)


def checkkey(servicename):
    return keyring.get_password(PKGNAME, servicename)


def deletekey(servicename):
    if KEYRINGALT:
        backend = keyrings.alt.file.EncryptedKeyring()
        keyring.set_keyring(backend)
    try:
        keyring.delete_password(PKGNAME, servicename)
    except Exception:
        pass
