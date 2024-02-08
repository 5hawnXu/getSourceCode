import argparse
from argparse import RawTextHelpFormatter
from getSourceCode.common import current_version


def argparse_menu():
    parser = argparse.ArgumentParser(
        description="To get contract source code verified on blockchain explorer. \n\n"
                    "Support network: \n"
                    "arbi|arbi-nova|avax|base|boba|bsc\n"
                    "bttc|celo|cronos|eth|fantom|gnosis\n"
                    "heco|klaytn|linea|moonbeam|moonriver\n"
                    "okt|opt|poly|poly-zk|ronin|tron|zkSyncEra\n\n"
                    "alfajores|arbi-testnet|avax-testnet\n"
                    "baobab|base-testnet|boba-testnet|bsc-testnet\n"
                    "bttc-testnet|ftm-testnet|goerli|heco-testnet\n"
                    "linea-testnet|moonbase|opt-testnet|okb\n"
                    "okt-testnet|poly-testnet|poly-zk-testnet\n"
                    "ronin-testnet|sepolia\n\n"
                    "Get code by tx only supports:\n"
                    "arbi|arbi-nova|avax|base|boba|bsc\n"
                    "cronos|eth|fantom|gnosis|heco|klaytn\n"
                    "moonbeam|moonriver|opt|poly||ronin\n"
                    "arbi-testnet|avax-testnet|base-testnet\n"
                    "boba-testnet|bsc-testnet|ftm-testnet\n"
                    "goerli|opt-testnet|poly-testnet\n\n"
                    "Some of the above networks may not be fully tested. \nIf you encounter any problems, please contact support@hxzy.me",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-i', default='', dest='inputFile', help='Input file path including contract addresses.')
    parser.add_argument('-o', default='', dest='outputFolder', help='Choose a folder to export.')
    parser.add_argument('-a', default='', dest='address', help='A string including contract addresses.')
    parser.add_argument('-n', default='', dest='network', help='Which network to get source code.')
    parser.add_argument('-k', action="store_true", dest='key', help='Provide some blockchain explorer api keys.')
    parser.add_argument('-p', default='', dest='proxy', help='Use a proxy.')
    parser.add_argument('-t', default='', dest='txhash', help='Get the relevant contract source code in the specified transaction.')
    parser.add_argument('-u', action="store_true", dest='update', help='Check to see if a new version is available to update.')
    parser.add_argument('-v', action='version', version=current_version, help='Show version')
    parser.add_argument('--apikey', default='', dest='apikey', help='The apikey required by the okex related chain.')

    return parser.parse_args()
