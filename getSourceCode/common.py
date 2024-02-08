import sys
import os
import time

# Package base info
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
current_version = "2.0.7"
name = "getSourceCode"
proxy_contract = {}
contract_index = 0
contract_info = {}
EXIT_CODE = 0
proxy = ""
deal_addresses = []

def print_okex_api_key_explain():
    print("If you want to get the contract code of the okex link, you need to manually enter the api key.\nVisit this link: \n1. okt: https://www.oklink.com/cn/oktc/address/0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE\n2. okb: https://www.oklink.com/cn/okbc-test/address/0x6BC26C28130e7634fFa1330969f34e98DC4d0019\n3. okt-testnet: https://www.oklink.com/cn/oktc-test/address/0x7c3ebCB6c4Ae99964980006C61d7eb032eDcb06B\n\nFollow the steps below:\n1. Open the above link\n2. Open the browser developer tool\n3. Click the contract tab page on the browser\n4. Find the request \"contract?t=\"\n5. X-Apikey in the request header of the request is the required apikey\n\nFor example:\ngetCode -p 127.0.0.1:7890 -n okt -a 0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE --apikey LWIzMWUtNDU0Ny05Mjk5LWI2ZDA3Yjc2MzFhYmEyYzkwM2NjfDI4MDQzNDU3Mjc2NjY0OTI=")
    sys.exit(EXIT_CODE)

    
def set_configs(input_proxy):
    global proxy
    proxy = input_proxy


def get_proxies():
    proxies = {}
    if proxy != "":
        proxies = {
            "https": "http://" + proxy,
            "http": "http://" + proxy
        }
    return proxies


def handle_exception(e):
    print("--------------------------------------")
    print("error line:", e.__traceback__.tb_lineno)
    print("error type:", e)
    print("--------------------------------------")
    sys.exit(EXIT_CODE)


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
