from audioop import add
import json
import base64
import requests
from getSourceCode.common import *
from getSourceCode.config import req_url
from getSourceCode.keys import get_key
from retrying import retry


def save_info(address, contract_name):
    try:
        if address not in contract_info.keys():
            contract_info[address] = contract_name
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def tron_requests(address, api_url):
    data = {
        "contractAddress": address
    }
    tron_req = requests.post(api_url, data=data)
    return tron_req


def send_tron(addresses, output_folder):
    global contract_index
    try:
        api_url = "https://apiasia.tronscan.io:5566/api/solidity/contract/info"
        for address in addresses:
            req = tron_requests(address, api_url)
            if json.loads(req.text)["code"] == 200:
                contract_code = json.loads(req.text)["data"]["contract_code"]
                contract_folder = json.loads(req.text)["data"][
                    "contract_name"] if output_folder == "" else output_folder
                make_dir(contract_folder)
                sub_index = 0
                save_info(address, json.loads(req.text)["data"]["contract_name"])
                for code in contract_code:
                    index = 0
                    contract_name = code['name']
                    while os.path.exists(contract_folder + "//" + contract_name):
                        if contract_name.find("_")!= -1:
                            contract_name = code['name'].split('_')[0] + "_{}".format(index) + ".sol"
                        else:
                            contract_name = code['name'].split('.')[0] + "_{}".format(index) + ".sol"
                        index += 1
                    make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
                    with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                        fw.write(str(base64.b64decode(code['code']), 'utf-8').replace('\r\n', '\n'))

                    print(f'{contract_index}-{sub_index}: {contract_folder + "/" + contract_name}'.replace(
                        '//', '/'))
                    sub_index += 1
            contract_index += 1
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def okex_requests(api_url, apikey, proxies):
    head = {
        "X-Apikey": apikey
    }
    okex_req = requests.get(api_url, headers=head, proxies=proxies)
    return okex_req


def send_okex(addresses, output_folder, apikey, network):
    okex_network_api = {
        "okt": "okexchain",
        "okb": "okbc_test",
        "okt-testnet": "okexchain_test"
    }
    global contract_index
    global proxy_contract
    proxies = get_proxies()
    try:
        for address in addresses:
            api_url = f"https://www.oklink.com/api/explorer/v1/{okex_network_api[network]}/addresses/{address}/contract"
            req = okex_requests(api_url, apikey, proxies)
            if json.loads(req.text)["code"] == 0:
                contractSourceList = json.loads(req.text)["data"]["contractSourceList"]
                contract_main_name = json.loads(req.text)["data"]["name"] if "name" in json.loads(req.text)[
                    "data"].keys() else "not_open_source"
                if contractSourceList != []:
                    contract_code_list = json.loads(req.text)["data"]["contractSourceList"]
                else:
                    contract_code_list = [{
                        "name": contract_main_name,
                        "source_code": json.loads(req.text)["data"]["contractSource"],
                    }]
                contract_folder = contract_main_name if output_folder == "" else output_folder
                make_dir(contract_folder)
                save_info(address, contract_main_name)
                sub_index = 0
                for code in contract_code_list:
                    index = 0
                    contract_name = code['name'] + ".sol"
                    while os.path.exists(contract_folder + "//" + contract_name):
                        if contract_name.find("_")!= -1:
                            contract_name = code['name'].split('_')[0] + "_{}".format(index) + ".sol"
                        else:
                            contract_name = code['name'].split('.')[0] + "_{}".format(index) + ".sol"
                        index += 1
                    make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
                    with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                        fw.write(code['source_code'].replace('\r\n', '\n'))
                    print(f'{contract_index}-{sub_index}: {contract_folder + "/" + contract_name}'.replace('//', '/'))
                    sub_index += 1
                contract_index += 1
                impl = ""
                if "implContractAddress" in json.loads(req.text)["data"].keys():
                    impl = json.loads(req.text)["data"]["implContractAddress"]
                if impl != "":
                    addresses = [impl]
                    proxy_contract[address] = impl
                    send_okex(addresses, "impl_contract", apikey, network)
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def klaytn_requests(real_url, proxies):
    klaytn_req = requests.get(real_url, proxies=proxies)
    return klaytn_req


def send_klaytn(addresses, output_folder, network):
    global contract_index
    try:
        proxies = get_proxies()
        for address in addresses:
            if network == "klaytn":
                klaytn_url = f"https://api-cypress.klaytnscope.com/v2/accounts/{address}"
            else:
                klaytn_url = f"https://api-baobab.klaytnscope.com/v2/accounts/{address}"
            req = klaytn_requests(klaytn_url, proxies)
            code = json.loads(req.text)['result']['matchedContract']
            contract_name = code['contractName'] + ".sol"
            save_info(address, code['contractName'])
            contract_folder = code['contractName'] if output_folder == "" else output_folder
            index = 0
            while os.path.exists(contract_folder + "//" + contract_name):
                if contract_name.find("_")!= -1:
                    contract_name = code['contractName'].split('_')[0] + "_{}".format(index) + ".sol"
                else:
                    contract_name = code['contractName'].split('.')[0] + "_{}".format(index) + ".sol"
                index += 1
            make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
            with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                fw.write(code["contractSource"].replace('\r\n', '\n'))
            print(f'{contract_index}: {contract_folder + "/" + contract_name}'.replace('//', '/'))
            contract_index += 1
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def check_ronin_is_proxy(address, proxies, network):
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    if network == "ronin":
        check_proxy_url = f"https://explorer-kintsugi.roninchain.com/v2/2020/contract/{address}"
    else:
        check_proxy_url = f"https://explorer-kintsugi.roninchain.com/v2/2021/contract/{address}"
    check_proxy_req = requests.get(check_proxy_url, proxies=proxies, headers=header)
    return check_proxy_req.json()['result']


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def ronin_request(url, proxies):
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    ronin_req = requests.get(url, proxies=proxies, headers=header)
    return ronin_req.json()


def send_ronin(addresses, output_folder, network):
    global contract_index
    global proxy_contract
    try:
        proxies = get_proxies()
        for address in addresses:
            address_info = check_ronin_is_proxy(address, proxies, network)
            proxy_address = address_info["proxy_to"]
            contract_name = address_info["contract_name"]
            if network == "ronin":
                url = f"https://explorer-kintsugi.roninchain.com/v2/2020/contract/{address}/src"
            else:
                url = f"https://explorer-kintsugi.roninchain.com/v2/2021/contract/{address}/src"
            ronin_req = ronin_request(url, proxies)
            save_info(address, contract_name)
            contract_folder = contract_name if output_folder == "" else output_folder
            index = 0
            sub_index = 0
            for code in ronin_req['result']:
                while os.path.exists(contract_folder + "//" + contract_name):
                    if contract_name.find("_")!= -1:
                        contract_name = contract_name.split('_')[0] + "_{}".format(index) + ".sol"
                    else:
                        contract_name = contract_name.split('.')[0] + "_{}".format(index) + ".sol"
                    index += 1
                make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
                with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                    fw.write(code['content'].replace('\r\n', '\n'))
                sub_index += 1
                print(f'{contract_index}-{sub_index}: {contract_folder + "/" + contract_name}'.replace('//', '/'))
            contract_index += 1
            if proxy_address != "":
                addresses = [proxy_address]
                proxy_contract[address] = proxy_address
                send_ronin(addresses, output_folder, network)
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def zksync_request(url, proxies):
    header = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    zksync_req = requests.get(url, proxies=proxies, headers=header)
    return zksync_req.json()


def send_zksync_era(addresses, output_folder, network):
    global contract_index
    global proxy_contract
    try:
        proxies = get_proxies()
        for address in addresses:
            if network == "zksyncera":
                url = f"https://zksync2-mainnet-explorer.zksync.io/contract_verification/info/{address}"
            else:
                url = f"https://zksync2-testnet-explorer.zksync.dev/contract_verification/info/{address}"
            zksync_req = zksync_request(url, proxies)
            contract_name = zksync_req['request']['contractName'].split(".sol:")[1]
            save_info(address, contract_name)
            contract_folder = contract_name if output_folder == "" else output_folder
            index = 0
            sub_index = 0
            for contract_name in zksync_req['request']['sourceCode']['sources'].keys():
                while os.path.exists(contract_folder + "//" + contract_name):
                    if contract_name.find("_")!= -1:
                        contract_name = contract_name.split('_')[0] + "_{}".format(index) + ".sol"
                    else:
                        contract_name = contract_name.split('.')[0] + "_{}".format(index) + ".sol"
                    index += 1
                make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
                with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                    fw.write(
                        zksync_req['request']['sourceCode']['sources'][contract_name]['content'].replace('\r\n', '\n'))
                sub_index += 1
                print(f'{contract_index}-{sub_index}: {contract_folder + "/" + contract_name}'.replace('//', '/'))
            contract_index += 1
    except Exception as e:
        handle_exception(e)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def common_requests(real_url, proxies, headers):
    common_req = requests.get(real_url, proxies=proxies, headers=headers)
    return common_req


def send_request(addresses, output_folder, network):
    try:
        proxies = get_proxies()
        headers = {
            'user-agent': USER_AGENT
        }
        for address in addresses:
            if address in deal_addresses:
                continue
            deal_addresses.append(address)
            output_data = ""
            real_url = req_url[network] + address + "&apikey=" + get_key(network)
            req = common_requests(real_url, proxies, headers)
            results = json.loads(req.text)['result']
            if isinstance(results, dict):
                output_data = results
            elif isinstance(results, list):
                output_data = results[0]
            export_result(output_data, output_folder, network, address)
    except Exception as e:
        handle_exception(e)


def export_result(result, output_folder, network, address):
    global contract_index
    global proxy_contract
    if "ContractName" not in result.keys():
        return
    try:
        contract_suffix = ".sol"
        if result['CompilerVersion'].find("vyper") != -1:
            contract_suffix = ".vy"
        index = 0
        sub_index = 0
        is_multi_file = False
        contract_name = result['ContractName']
        save_info(address, contract_name)
        source_code = result['SourceCode'].replace("\r\n", "\n")
        if source_code.find(contract_suffix + '":{"content":') != -1:
            is_multi_file = True
        if "\"language\":" in source_code or is_multi_file:
            contract_folder = contract_name if output_folder == "" else output_folder
            make_dir(contract_folder)
            if not is_multi_file:
                source_code = json.loads(source_code[1:-1])['sources']
            else:
                source_code = json.loads(source_code)
            for key in source_code.keys():
                contract_name = key + contract_suffix if key.find(contract_suffix) == -1 else key
                while os.path.exists(contract_folder + "//" + contract_name):
                    if contract_name.find("_")!= -1:
                        contract_name = contract_name.split('_')[0] + "_{}".format(index) + ".sol"
                    else:
                        contract_name = contract_name.split('.')[0] + "_{}".format(index) + ".sol"
                    index += 1
                index = 0
                make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
                with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                    fw.write(source_code[key]["content"].replace('\r\n', '\n'))
                print(f'{contract_index}-{sub_index}: {contract_folder + "/" + contract_name}'.replace('//', '/'))
                sub_index += 1
            contract_index += 1
        else:
            if contract_name == "":
                return
            contract_folder = contract_name if output_folder == "" else output_folder
            contract_name = contract_name + contract_suffix if contract_name.find(contract_suffix) == -1 else contract_name
            while os.path.exists(contract_folder + "//" + contract_name):
                if contract_name.find("_")!= -1:
                        contract_name = contract_name.split('_')[0] + "_{}".format(index) + ".sol"
                else:
                    contract_name = contract_name.split('.')[0] + "_{}".format(index) + ".sol"
                index += 1
            make_dir(os.path.split(contract_folder + "//" + contract_name)[0])
            with open(contract_folder + "//" + contract_name, "w+", encoding='utf-8') as fw:
                fw.write(source_code.replace('\r\n', '\n'))
            print(f'{contract_index}-{sub_index}: {contract_folder + "/" + contract_name}'.replace('//', '/'))
            contract_index += 1
        addresses = []
        if network == "cronos":
            if "ImplementationAddress" in result.keys():
                if result['ImplementationAddress'] != "":
                    proxy_contract[address] = result['ImplementationAddress']
                    addresses.append(result['ImplementationAddress'])
                    send_request(addresses, "Implementation", network)
        elif result['Implementation'] != "":
            # Handle block explorer API exception returns to avoid infinite loops
            if result['Implementation'].lower() == address.lower():
                return
            proxy_contract[address] = result['Implementation']
            addresses.append(result['Implementation'])
            send_request(addresses, "Implementation", network)
    except Exception as e:
        handle_exception(e)
