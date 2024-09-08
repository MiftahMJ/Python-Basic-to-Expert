# proxy_config.py

# Proxy credentials and endpoint
PROXY_USERNAME = "yabada_djkVV"
PROXY_PASSWORD = "yuhimR42_yabada"
ENDPOINT = "pr.oxylabs.io:7777"

def get_proxy_options() -> dict:
    """Returns a dictionary with proxy settings for Selenium Wire."""
    wire_options = {
        "proxy": {
            "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{ENDPOINT}",
            "https": f"https://{PROXY_USERNAME}:{PROXY_PASSWORD}@{ENDPOINT}",
        }
    }
    return wire_options
