import json
import base64
import requests
from getsourcecode.common import *
from getsourcecode.config import *
from getsourcecode.keys import get_key
from tenacity import retry, stop_after_attempt, wait_fixed


def check_is_duplicate_file(file_path, contract_code):
    if hash_file(file_path) == hash_string(contract_code):
        return True
    return False


def get_unique_contract_folder(base_name, address, ctx=None):
    """Generate a unique folder name when contract names conflict in the same batch."""
    target = ctx.contract_info if ctx else contract_info
    for addr, name in target.items():
        if name == base_name and addr.lower() != address.lower():
            short_addr = address[:6]
            return f"{base_name}_{short_addr}"
    return base_name


def save_contract_file(contract_folder, original_name, code_content):
    """
    Generic function to save contract files.

    Args:
        contract_folder: Directory to save the file
        original_name: Original filename
        code_content: File content

    Returns:
        Saved filename, or None if skipped
    """
    contract_name = original_name
    index = 0
    exist_file = False

    # Handle filename conflicts
    file_path = os.path.join(contract_folder, contract_name)
    while os.path.exists(file_path):
        exist_file = True
        dir_part = os.path.dirname(original_name)
        file_part = os.path.basename(original_name)
        name_without_ext, ext = os.path.splitext(file_part)
        if not ext:
            ext = ".sol"
        contract_name = os.path.join(dir_part, f"{name_without_ext}_{index}{ext}")
        file_path = os.path.join(contract_folder, contract_name)
        index += 1

    # Check for duplicate content
    original_path = os.path.join(contract_folder, original_name)
    if exist_file and os.path.exists(original_path):
        if check_is_duplicate_file(original_path, code_content):
            return None  # Skip duplicate file

    # Create directory and write file
    make_dir(os.path.dirname(file_path))
    with open(file_path, "w+", encoding='utf-8') as fw:
        fw.write(code_content)

    return contract_name


def save_info(address, contract_name, ctx=None):
    try:
        target = ctx.contract_info if ctx else contract_info
        if address not in target:
            target[address] = contract_name
    except Exception as e:
        handle_exception(e)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def tron_requests(address, api_url):
    data = {
        "contractAddress": address
    }
    tron_req = requests.post(api_url, data=data, verify=False)
    return tron_req


def send_tron(addresses, output_folder, ctx=None):
    global contract_index
    try:
        api_url = "https://apiasia.tronscan.io:5566/api/solidity/contract/info"
        for address in addresses:
            req = tron_requests(address, api_url)
            if json.loads(req.text)["code"] == 200:
                contract_code = json.loads(req.text)["data"]["contract_code"]
                contract_folder = get_unique_contract_folder(
                    json.loads(req.text)["data"]["contract_name"], address, ctx
                ) if output_folder == "" else output_folder
                make_dir(contract_folder)
                sub_index = 0
                save_info(address, json.loads(req.text)["data"]["contract_name"], ctx)
                c_idx = ctx.contract_index if ctx else contract_index
                for code in contract_code:
                    contract_name = code['name']
                    code_temp = str(base64.b64decode(code['code']), 'utf-8').replace('\r\n', '\n')
                    saved_name = save_contract_file(contract_folder, contract_name, code_temp)
                    if saved_name:
                        print(f'{c_idx}-{sub_index}: {contract_folder}/{saved_name}')
                        sub_index += 1
            if ctx:
                ctx.contract_index += 1
            else:
                contract_index += 1
    except Exception as e:
        handle_exception(e)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def okex_requests(api_url, apikey, proxies):
    head = {
        "X-Apikey": apikey
    }
    okex_req = requests.get(api_url, headers=head, proxies=proxies, verify=False)
    return okex_req


def send_okex(addresses, output_folder, apikey, network, ctx=None):
    okex_network_api = {
        "okt": "okexchain",
        "okb": "okbc_test",
        "okt-testnet": "okexchain_test"
    }
    global contract_index
    global proxy_contract
    proxies = get_proxies(ctx)
    try:
        for address in addresses:
            api_url = f"https://www.oklink.com/api/explorer/v1/{okex_network_api[network]}/addresses/{address}/contract"
            req = okex_requests(api_url, apikey, proxies)
            if json.loads(req.text)["code"] == 0:
                data = json.loads(req.text)["data"]
                contractSourceList = data.get("contractSourceList", [])
                contract_main_name = data.get("name", "not_open_source")
                if contractSourceList:
                    contract_code_list = contractSourceList
                else:
                    contract_code_list = [{
                        "name": contract_main_name,
                        "source_code": data.get("contractSource", ""),
                    }]
                contract_folder = get_unique_contract_folder(contract_main_name, address, ctx) if output_folder == "" else output_folder
                make_dir(contract_folder)
                save_info(address, contract_main_name, ctx)
                sub_index = 0
                c_idx = ctx.contract_index if ctx else contract_index
                for code in contract_code_list:
                    contract_name = code['name'] + ".sol"
                    code_temp = code['source_code'].replace('\r\n', '\n')
                    saved_name = save_contract_file(contract_folder, contract_name, code_temp)
                    if saved_name:
                        print(f'{c_idx}-{sub_index}: {contract_folder}/{saved_name}')
                        sub_index += 1
                if ctx:
                    ctx.contract_index += 1
                else:
                    contract_index += 1
                impl = data.get("implContractAddress", "")
                if impl:
                    impl_addresses = [impl]
                    if ctx:
                        ctx.proxy_contract[address] = impl
                    else:
                        proxy_contract[address] = impl
                    send_okex(impl_addresses, os.path.join(contract_folder, "Implementation"), apikey, network, ctx)
    except Exception as e:
        handle_exception(e)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def klaytn_requests(real_url, proxies):
    klaytn_req = requests.get(real_url, proxies=proxies, verify=False)
    return klaytn_req


def send_klaytn(addresses, output_folder, network, ctx=None):
    global contract_index
    try:
        proxies = get_proxies(ctx)
        for address in addresses:
            if network == "klaytn":
                klaytn_url = f"https://api-cypress.klaytnscope.com/v2/accounts/{address}"
            else:
                klaytn_url = f"https://api-baobab.klaytnscope.com/v2/accounts/{address}"
            req = klaytn_requests(klaytn_url, proxies)
            code = json.loads(req.text)['result']['matchedContract']
            contract_name = code['contractName'] + ".sol"
            code_temp = code["contractSource"].replace('\r\n', '\n')
            save_info(address, code['contractName'], ctx)
            contract_folder = get_unique_contract_folder(code['contractName'], address, ctx) if output_folder == "" else output_folder
            make_dir(contract_folder)
            c_idx = ctx.contract_index if ctx else contract_index
            saved_name = save_contract_file(contract_folder, contract_name, code_temp)
            if saved_name:
                print(f'{c_idx}: {contract_folder}/{saved_name}')
                if ctx:
                    ctx.contract_index += 1
                else:
                    contract_index += 1
    except Exception as e:
        handle_exception(e)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def check_ronin_is_proxy(address, proxies, network):
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    if network == "ronin":
        check_proxy_url = f"https://explorer-kintsugi.roninchain.com/v2/2020/contract/{address}"
    else:
        check_proxy_url = f"https://explorer-kintsugi.roninchain.com/v2/2021/contract/{address}"
    check_proxy_req = requests.get(check_proxy_url, proxies=proxies, headers=header, verify=False)
    return check_proxy_req.json()['result']


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def ronin_request(url, proxies):
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    ronin_req = requests.get(url, proxies=proxies, headers=header, verify=False)
    return ronin_req.json()


def send_ronin(addresses, output_folder, network, ctx=None):
    global contract_index
    global proxy_contract
    try:
        proxies = get_proxies(ctx)
        for address in addresses:
            address_info = check_ronin_is_proxy(address, proxies, network)
            proxy_address = address_info["proxy_to"]
            contract_name = address_info["contract_name"]
            if network == "ronin":
                url = f"https://explorer-kintsugi.roninchain.com/v2/2020/contract/{address}/src"
            else:
                url = f"https://explorer-kintsugi.roninchain.com/v2/2021/contract/{address}/src"
            ronin_req = ronin_request(url, proxies)
            save_info(address, contract_name, ctx)
            contract_folder = get_unique_contract_folder(contract_name, address, ctx) if output_folder == "" else output_folder
            make_dir(contract_folder)
            sub_index = 0
            c_idx = ctx.contract_index if ctx else contract_index
            for code in ronin_req['result']:
                file_name = code.get('name', contract_name)
                code_temp = code['content'].replace('\r\n', '\n')
                saved_name = save_contract_file(contract_folder, file_name, code_temp)
                if saved_name:
                    print(f'{c_idx}-{sub_index}: {contract_folder}/{saved_name}')
                    sub_index += 1
            if ctx:
                ctx.contract_index += 1
            else:
                contract_index += 1
            if proxy_address:
                proxy_addresses = [proxy_address]
                if ctx:
                    ctx.proxy_contract[address] = proxy_address
                else:
                    proxy_contract[address] = proxy_address
                send_ronin(proxy_addresses, os.path.join(contract_folder, "Implementation"), network, ctx)
    except Exception as e:
        handle_exception(e)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def zksync_request(url, proxies):
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    zksync_req = requests.get(url, proxies=proxies, headers=header, verify=False)
    return zksync_req.json()


def send_zksync_era(addresses, output_folder, network, ctx=None):
    global contract_index
    try:
        proxies = get_proxies(ctx)
        for address in addresses:
            if network == "zksyncera":
                url = f"https://zksync2-mainnet-explorer.zksync.io/contract_verification/info/{address}"
            else:
                url = f"https://zksync2-testnet-explorer.zksync.dev/contract_verification/info/{address}"
            zksync_req = zksync_request(url, proxies)
            main_contract_name = zksync_req['request']['contractName'].split(".sol:")[1]
            save_info(address, main_contract_name, ctx)
            contract_folder = get_unique_contract_folder(main_contract_name, address, ctx) if output_folder == "" else output_folder
            make_dir(contract_folder)
            sub_index = 0
            c_idx = ctx.contract_index if ctx else contract_index
            sources = zksync_req['request']['sourceCode']['sources']
            for file_name, source_data in sources.items():
                code_temp = source_data['content'].replace('\r\n', '\n')
                saved_name = save_contract_file(contract_folder, file_name, code_temp)
                if saved_name:
                    print(f'{c_idx}-{sub_index}: {contract_folder}/{saved_name}')
                    sub_index += 1
            if ctx:
                ctx.contract_index += 1
            else:
                contract_index += 1
    except Exception as e:
        handle_exception(e)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def common_requests(real_url, proxies, headers):
    common_req = requests.get(real_url, proxies=proxies, headers=headers, verify=False)
    return common_req


def send_request(addresses, output_folder, network, api_key, ctx=None):
    global deal_addresses
    try:
        proxies = get_proxies(ctx)
        headers = {
            'user-agent': USER_AGENT
        }
        for address in addresses:
            dealt = ctx.deal_addresses if ctx else deal_addresses
            if address in dealt:
                continue
            if ctx:
                ctx.deal_addresses.append(address)
            else:
                deal_addresses.append(address)
            output_data = ""
            api_key = get_key() if api_key == "" else api_key
            real_url = req_url + address + "&apikey=" + api_key + f"&chainid={chain_to_id.get(network)}"
            req = common_requests(real_url, proxies, headers)
            results = json.loads(req.text)['result']
            if isinstance(results, dict):
                output_data = results
            elif isinstance(results, list):
                output_data = results[0]
            export_result(output_data, output_folder, network, address, api_key, ctx)
    except Exception as e:
        handle_exception(e)


def export_result(result, output_folder, network, address, api_key, ctx=None):
    global contract_index
    global proxy_contract
    if not isinstance(result, dict) or "ContractName" not in result:
        return
    try:
        contract_suffix = ".sol"
        if "vyper" in result.get('CompilerVersion', ''):
            contract_suffix = ".vy"
        sub_index = 0
        is_multi_file = False
        main_contract_name = result['ContractName']
        save_info(address, main_contract_name, ctx)
        source_code = result['SourceCode'].replace("\r\n", "\n")
        if (contract_suffix + '":{"content":') in source_code:
            is_multi_file = True
        contract_folder = get_unique_contract_folder(main_contract_name, address, ctx) if output_folder == "" else output_folder
        make_dir(contract_folder)
        c_idx = ctx.contract_index if ctx else contract_index

        if "\"language\":" in source_code or is_multi_file:
            # Multi-file contract
            if not is_multi_file:
                sources = json.loads(source_code[1:-1])['sources']
            else:
                sources = json.loads(source_code)
            for key, source_data in sources.items():
                file_name = key + contract_suffix if contract_suffix not in key else key
                code_temp = source_data["content"].replace('\r\n', '\n')
                saved_name = save_contract_file(contract_folder, file_name, code_temp)
                if saved_name:
                    print(f'{c_idx}-{sub_index}: {contract_folder}/{saved_name}')
                    sub_index += 1
            if ctx:
                ctx.contract_index += 1
            else:
                contract_index += 1
        else:
            # Single-file contract
            if main_contract_name == "":
                return
            file_name = main_contract_name + contract_suffix if contract_suffix not in main_contract_name else main_contract_name
            code_temp = source_code.replace('\r\n', '\n')
            saved_name = save_contract_file(contract_folder, file_name, code_temp)
            if saved_name:
                print(f'{c_idx}-{sub_index}: {contract_folder}/{saved_name}')
                if ctx:
                    ctx.contract_index += 1
                else:
                    contract_index += 1

        # Handle proxy contracts
        impl_addresses = []
        if network == "cronos":
            impl = result.get('ImplementationAddress', '')
            if impl:
                if ctx:
                    ctx.proxy_contract[address] = impl
                else:
                    proxy_contract[address] = impl
                impl_addresses.append(impl)
                send_request(impl_addresses, os.path.join(contract_folder, "Implementation"), network, api_key, ctx)
        elif result['Implementation'] != "":
            # Handle block explorer API exception returns to avoid infinite loops
            if result['Implementation'].lower() == address.lower():
                return
            if ctx:
                ctx.proxy_contract[address] = result['Implementation']
            else:
                proxy_contract[address] = result['Implementation']
            impl_addresses.append(result['Implementation'])
            send_request(impl_addresses, os.path.join(contract_folder, "Implementation"), network, api_key, ctx)
    except Exception as e:
        handle_exception(e)
