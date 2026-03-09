# -*- coding: utf-8 -*-
from getsourcecode.check import *
from getsourcecode.filter import *
from getsourcecode.config import *
from getsourcecode.keys import *
from getsourcecode.common import *
import getsourcecode.menu
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Load config
parser = menu.argparse_menu()


def get_code(input_file, output_folder, address, network, api_key, ctx=None):
    try:
        if network.lower() == "Tron".lower():
            addresses = get_addresses_by_file_or_string(input_file, True, address)
            send_tron(addresses, output_folder, ctx)
        elif network.lower() == "okt" or network.lower() == "okt-testnet" or network.lower() == "okb":
            if parser.apikey == "":
                print_okex_api_key_explain()
                return
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_okex(addresses, output_folder, parser.apikey, network.lower(), ctx)
        elif network.lower() == "klaytn" or network.lower() == "baobab":
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_klaytn(addresses, output_folder, network, ctx)
        elif network.lower() == "ronin" or network.lower() == "ronin-testnet":
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_ronin(addresses, output_folder, network, ctx)
        elif network.lower() == "zksyncera" or network.lower() == "zksyncera-testnet":
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_zksync_era(addresses, output_folder, network, ctx)
        else:
            if network in paid_only_set and api_key == "":
                raise ValueError("Invalid api key, please privide paid api key")
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            if addresses:
                send_request(addresses, output_folder, network, api_key, ctx)
            else:
                raise ValueError("Error address")
    except Exception as e:
        handle_exception(e)


def main():
    # Create download context
    ctx = DownloadContext()
    try:
        if parser.proxy:
            set_configs(parser.proxy, ctx)
        # Resolve --chainid to network name if provided
        network = parser.network
        if parser.chainid:
            if parser.chainid in chain_id_to_name:
                network = chain_id_to_name[parser.chainid]
            else:
                network = f"chain-{parser.chainid}"
                chain_to_id[network] = parser.chainid
        if parser.update:
            check_update(name, current_version)
            sys.exit(0)
        elif parser.inputFile != "" or parser.address != "":
            get_code(parser.inputFile, parser.outputFolder, parser.address, network.lower(), parser.key, ctx)
        elif parser.txhash != "":
            get_addresses_by_tx(parser.txhash, network.lower(), parser.outputFolder, ctx)
        else:
            print("Invalid command")
        if ctx.contract_info != {}:
            print("\nAddress => ContractName:")
            for key in ctx.contract_info.keys():
                print(f"{key}\t{ctx.contract_info[key]}")
        if ctx.proxy_contract != {}:
            print("\nProxy => Implementation:")
            for key in ctx.proxy_contract.keys():
                print(f"{key}\t{ctx.proxy_contract[key]}")
        print('\nSuccess.')
    except Exception as e:
        handle_exception(e)


if __name__ == '__main__':
    main()
