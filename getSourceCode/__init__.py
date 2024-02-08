# -*- coding: utf-8 -*-
from getSourceCode.check import *
from getSourceCode.filter import *
from getSourceCode.config import *
from getSourceCode.keys import *
from getSourceCode.common import *
import getSourceCode.menu

# Load config
parser = menu.argparse_menu()


def get_code(input_file, output_folder, address, network):
    try:
        if network.lower() == "Tron".lower():
            addresses = get_addresses_by_file_or_string(input_file, True, address)
            send_tron(addresses, output_folder)
        elif network.lower() == "okt" or network.lower() == "okt-testnet" or network.lower() == "okb":
            if parser.apikey == "":
                print_okex_api_key_explain()
                return
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_okex(addresses, output_folder, parser.apikey, network.lower())
        elif network.lower() == "klaytn" or network.lower() == "baobab":
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_klaytn(addresses, output_folder, network)
        elif network.lower() == "ronin" or network.lower() == "ronin-testnet":
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_ronin(addresses, output_folder, network)
        elif network.lower() == "zksyncera" or network.lower() == "zksyncera-testnet":
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            send_zksync_era(addresses, output_folder, network)
        else:
            valid_keys = get_keys(network)
            if not valid_keys and valid_keys != []:
                raise ValueError("Invalid network")
            addresses = get_addresses_by_file_or_string(input_file, False, address)
            if addresses:
                send_request(addresses, output_folder, network)
            else:
                raise ValueError("Error address")
    except Exception as e:
        handle_exception(e)


def main():
    try:
        if parser.proxy:
            set_configs(parser.proxy)
        if parser.update:
            check_update(name, current_version)
            sys.exit(0)
        elif parser.key:
            print_key(parser.network.lower())
            sys.exit(0)
        elif parser.inputFile != "" or parser.address != "":
            get_code(parser.inputFile, parser.outputFolder, parser.address, parser.network.lower())
        elif parser.txhash != "":
            get_addresses_by_tx(parser.txhash, parser.network.lower(), parser.outputFolder)
        else:
            print("Invalid command")
        if contract_info != {}:
            print("\nAddress => ContractName:")
            for key in contract_info.keys():
                print(f"{key}\t{contract_info[key]}")
        if proxy_contract != {}:
            print("\nProxy => Implementation:")
            for key in proxy_contract.keys():
                print(f"{key}\t{proxy_contract[key]}")
        print('\nSuccess.')
    except Exception as e:
        handle_exception(e)


if __name__ == '__main__':
    main()
