import sys
import os
import hashlib
import traceback

# Package base info
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
current_version = "3.0.1"
name = "getsourcecode"
EXIT_CODE = 0


class DownloadContext:
    """Encapsulates all state during the download process."""
    def __init__(self):
        self.proxy_contract = {}      # Proxy contract mapping {proxy_address: impl_address}
        self.contract_index = 0       # Contract counter
        self.contract_info = {}       # Contract address to name mapping
        self.deal_addresses = []      # List of processed addresses
        self.proxy = ""               # HTTP proxy configuration

    def get_proxies(self):
        """Get HTTP proxy configuration."""
        if self.proxy:
            return {
                "https": "http://" + self.proxy,
                "http": "http://" + self.proxy
            }
        return {}

    def reset(self):
        """Reset state for a new download task."""
        self.proxy_contract = {}
        self.contract_index = 0
        self.contract_info = {}
        self.deal_addresses = []


# Global default context (for backward compatibility)
_default_ctx = DownloadContext()

# Backward compatible global variables (deprecated, will be removed in future versions)
proxy_contract = _default_ctx.proxy_contract
contract_index = 0
contract_info = _default_ctx.contract_info
temp_contract_name = ""
find_duplicate_file = False
proxy = ""
deal_addresses = _default_ctx.deal_addresses

def print_okex_api_key_explain():
    print("If you want to get the contract code of the okex link, you need to manually enter the api key.\nVisit this link: \n1. okt: https://www.oklink.com/cn/oktc/address/0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE\n2. okb: https://www.oklink.com/cn/okbc-test/address/0x6BC26C28130e7634fFa1330969f34e98DC4d0019\n3. okt-testnet: https://www.oklink.com/cn/oktc-test/address/0x7c3ebCB6c4Ae99964980006C61d7eb032eDcb06B\n\nFollow the steps below:\n1. Open the above link\n2. Open the browser developer tool\n3. Click the contract tab page on the browser\n4. Find the request \"contract?t=\"\n5. X-Apikey in the request header of the request is the required apikey\n\nFor example:\ngetCode -p 127.0.0.1:7890 -n okt -a 0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE --apikey LWIzMWUtNDU0Ny05Mjk5LWI2ZDA3Yjc2MzFhYmEyYzkwM2NjfDI4MDQzNDU3Mjc2NjY0OTI=")
    sys.exit(EXIT_CODE)

    
def set_configs(input_proxy, ctx=None):
    global proxy
    proxy = input_proxy
    if ctx is None:
        _default_ctx.proxy = input_proxy
    else:
        ctx.proxy = input_proxy


def get_proxies(ctx=None):
    if ctx is not None:
        return ctx.get_proxies()
    proxies = {}
    if proxy != "":
        proxies = {
            "https": "http://" + proxy,
            "http": "http://" + proxy
        }
    return proxies


def handle_exception(e):
    print("--------------------------------------")
    traceback.print_exc()
    print("--------------------------------------")
    sys.exit(EXIT_CODE)

def hash_file(file_path, algorithm='sha256'):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    hash_result = hash_string(text, algorithm)
    return hash_result

def hash_string(text, algorithm='sha256'):
    h = hashlib.new(algorithm)
    h.update(text.encode('utf-8'))
    return h.hexdigest()



def make_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except OSError:
            return False
    else:
        return False
