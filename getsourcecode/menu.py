import argparse
from argparse import RawTextHelpFormatter
from getsourcecode.common import current_version


def argparse_menu():
    parser = argparse.ArgumentParser(
        description="To get contract source code verified on blockchain explorer.\n\n"
                    "Supported Chain Platforms:\n"
                    "    Ethereum Mainnet | Sepolia Testnet | Hoodi Testnet\n"
                    "    BNB Smart Chain Mainnet | BNB Smart Chain Testnet\n"
                    "    Polygon Mainnet | Polygon Amoy Testnet\n"
                    "    Base Mainnet | Base Sepolia Testnet\n"
                    "    Arbitrum One Mainnet | Arbitrum Sepolia Testnet\n"
                    "    Linea Mainnet | Linea Sepolia Testnet\n"
                    "    Blast Mainnet | Blast Sepolia Testnet\n"
                    "    OP Mainnet | OP Sepolia Testnet\n"
                    "    Avalanche C-Chain | Avalanche Fuji Testnet\n"
                    "    BitTorrent Chain Mainnet | BitTorrent Chain Testnet\n"
                    "    Celo Mainnet | Celo Sepolia Testnet\n"
                    "    Fraxtal Mainnet | Fraxtal Hoodi Testnet\n"
                    "    Gnosis\n"
                    "  * Chain names are case-insensitive.\n"
                    "  * Some chains (e.g. BNB Smart Chain, Base, OP, Avalanche) require a paid API plan.\n"
                    "  * For the full list, visit: https://docs.etherscan.io/supported-chains\n\n"
                    "Some of the above networks may not be fully tested.\n"
                    "If you encounter any problems, please contact support@hxzy.me\n\n"
                    "PS: Files with exactly the same code will not be saved repeatedly.",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-i', default='', dest='inputFile', help='Input file path including contract addresses.')
    parser.add_argument('-o', default='', dest='outputFolder', help='Choose a folder to export.')
    parser.add_argument('-a', default='', dest='address', help='A string including contract addresses.')
    parser.add_argument('-n', default='', dest='network', help='Which network to get source code.')
    parser.add_argument('-k', default='', dest='key', help='Provide paid api key to download paid-only network code.')
    parser.add_argument('-p', default='', dest='proxy', help='Use a proxy.')
    parser.add_argument('-t', default='', dest='txhash', help='Get the relevant contract source code in the specified transaction.')
    parser.add_argument('-u', action="store_true", dest='update', help='Check to see if a new version is available to update.')
    parser.add_argument('-v', action='version', version=current_version, help='Show current version.')
    parser.add_argument('--hash', action="store_true", dest='contractHash', help='Show contract hash data.')
    parser.add_argument('--apikey', default='', dest='apikey', help='The apikey required by the okex related chain.')

    return parser.parse_args()
