import re
from getSourceCode.handle import *
from getSourceCode.config import *
from retrying import retry

current_path = os.getcwd()
ADDRESS_PATTERN = r'[\'\"]{1}[\s]{0,5}:[\s]{0,5}[\'\"]{1}(0x[a-zA-Z0-9)]{40})[\'\"]{1}'


def get_address(json_data):
    try:
        address_list = list(set(re.findall(ADDRESS_PATTERN, json_data)))
        return address_list
    except Exception as e:
        handle_exception(e)


def read_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as fr:
            return fr.read().replace('\n', ' ')
    else:
        raise FileNotFoundError("File not found: {}".format(file_path))


def get_addresses_from_input(input_file, add_string):
    if input_file:
        file_path = os.path.join(current_path, input_file)
        add_str = read_file(file_path)
    elif add_string:
        add_str = add_string
    else:
        return None
    return add_str


def get_addresses_by_file_or_string(input_file, is_tron, add_string,):
    try:
        add_str = get_addresses_from_input(input_file, add_string)
        if add_str is None:
            return None

        if is_tron:
            pattern = r'T[a-zA-Z\d]{33}'
        else:
            pattern = r'0x[a-zA-Z\d]{40}'

        addresses = re.findall(pattern, add_str)
        return addresses
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_by_tenderly_api_use_retry(tx_hash, proxies, network):
    tenderly_api = f'https://api.tenderly.co/api/v1/public-contract/{tenderly_chain_id_list[network]}/tx/{tx_hash}'
    tenderly_req = requests.get(tenderly_api, proxies=proxies)
    return tenderly_req.json()['addresses']


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_by_scan_use_re_use_retry(url, proxies):
    header = {
        "User-Agent": USER_AGENT
    }
    scan_req = requests.get(url, headers=header, proxies=proxies)
    return scan_req


def get_by_scan_use_re(tx_hash, proxies, network):
    try:
        url = tx_hash_scan_config[network]['url'].format(tx_hash)
        scan_req = get_by_scan_use_re_use_retry(url, proxies)
        if tx_hash_scan_config[network]['re'] != "":
            data = scan_req.text.replace("\r\n", "").replace(' ', '').replace('\n', '')
            result = re.findall(r"{}".format(tx_hash_scan_config[network]['re']), data)[0]
        else:
            result = "{}".format(scan_req.json()["data"]["overview"]["internalTxns"])
        if network == 'eth':
            result = "[" + result + "]"
        scan_address_list = get_address(result)
        return scan_address_list
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_ronin_info_by_api_use_retry(tx_hash, start_index, size, header, proxies):
    ronin_api = f'https://explorerv3-api.roninchain.com/tx/{tx_hash}/internal?from={start_index}&size={size}'
    ronin_req = requests.get(ronin_api, headers=header, proxies=proxies)
    return ronin_req


def get_by_special_way_ronin(tx_hash, proxies):
    special_way_ronin_address_list = []
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    try:
        start_index = 0
        size = 25
        while True:
            ronin_req = get_ronin_info_by_api_use_retry(tx_hash, start_index, size, header, proxies)
            for ronin_item in ronin_req.json()['results']:
                special_way_ronin_address_list.append(ronin_item['from'])
                special_way_ronin_address_list.append(ronin_item['to'])
            total = ronin_req.json()["total"]
            rest = total - (start_index + 1) * 25
            if rest <= 0:
                break
            start_index = start_index + size
        return special_way_ronin_address_list
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_klaytn_block_by_api_use_retry(tx_hash, proxies):
    klaytn_block_api = f"https://api-cypress.klaytnscope.com/v2/txs/{tx_hash}"
    klaytn_block_req = requests.get(klaytn_block_api, proxies=proxies)
    return klaytn_block_req.json()["result"]["blockNumber"]


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_klaytn_trance_by_api_use_retry(tx_hash, proxies, klaytn_block):
    klaytn_trance_api = f"https://api-cypress.klaytnscope.com/v2/blocks/{klaytn_block}/itxDetail?txHash={tx_hash}"
    klaytn_trance_req = requests.get(klaytn_trance_api, proxies=proxies)
    return klaytn_trance_req


def get_by_special_way_klaytn(tx_hash, proxies):
    special_way_klaytn_address_list = []
    try:
        klaytn_block = get_klaytn_block_by_api_use_retry(tx_hash, proxies)
        klaytn_trance_req = get_klaytn_trance_by_api_use_retry(tx_hash, proxies, klaytn_block)
        for klaytn_item in klaytn_trance_req.json()["result"]:
            special_way_klaytn_address_list.append(klaytn_item['fromAddress'])
            special_way_klaytn_address_list.append(klaytn_item['toAddress'])
        return special_way_klaytn_address_list
    except Exception as e:
        handle_exception(e)


def get_by_special_way(tx_hash, proxies, network):
    special_address_list = []
    if network == "ronin":
        special_address_list = get_by_special_way_ronin(tx_hash, proxies)
    elif network == "klaytn":
        special_address_list = get_by_special_way_klaytn(tx_hash, proxies)
    return special_address_list


def get_addresses_by_tx(tx_hash, network, output_folder):
    temp_addresses_list = []
    proxies = get_proxies()
    if network in tenderly_chain_id_list.keys():
        temp_addresses_list = get_by_tenderly_api_use_retry(tx_hash, proxies, network)
    elif network in tx_hash_scan_config.keys():
        temp_addresses_list = get_by_scan_use_re(tx_hash, proxies, network)
    elif network in special_trace_api.keys():
        temp_addresses_list = get_by_special_way(tx_hash, proxies, network)

    if temp_addresses_list:
        temp_addresses_list = list(set(temp_addresses_list))
        send_request(temp_addresses_list, output_folder, network)
    else:
        print(f"{network} is not supported (at least for now).")
