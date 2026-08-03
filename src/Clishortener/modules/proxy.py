import subprocess
import tempfile
import os


def proxyconfig() -> dict:
    """
    Opens system default editor (or nano) with a template,
    and returns parsed proxy dict upon saving.
    """
    template = (
        "# Edit proxy settings below.\n"
        "# Lines starting with '#' will be ignored.\n"
        "Http=\n"
        "Https=\n"
    )
    with tempfile.NamedTemporaryFile(
        suffix=".tmp",
        mode="w+",
        delete=False
    ) as tf:
        tf.write(template)
        temp_path = tf.name
    try:
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, temp_path], check=True)
        proxies = {}
        with open(temp_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.lower().strip()
                    value = value.strip()
                    if value and key in ["http", "https"]:
                        proxies[key] = value
            return proxies

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
