class CaseInsensitiveDict(dict):
    def __init__(self, data=None):
        super().__init__()
        if data:
            for key, value in data.items():
                self[key] = value

    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())

    def get(self, key, default=None):
        return super().get(key.lower(), default)

api_keys = [
    "B69GNP1IXCXJUGTWVCZPW4PS6KFDQ9MNJ1",
    "TRUHXX8K4D5E4665M22FUYZ6F4ZP4SC6UQ",
    "373ZPPAM1QZYS55Q5AW24BKW124BGPMPIA",
    "75FE5RHNXQJPRY6A4EGXTWJKE4M7783W6F",
    "TRUHXX8K4D5E4665M22FUYZ6F4ZP4SC6UQ",
    "Q8K1J5WIXHVQWV1XHVFF1INTPHWFZP5AZV",
    "KWPEX5CZ437P2JRB2U7WZ37VQFAVZFXXP6"
]

req_url = "https://api.etherscan.io/v2/api?module=contract&action=getsourcecode&address="

tx_hash_scan_config = {
    'eth': {
        "url": "https://etherscan.io/vmtrace?txhash={}&type=parity#raw",
        "re": r"<preid=\"editor\"class=\"ms-3\">(.*?)</pre>"
    },
    'bsc': {
        "url": "https://www.bscscan.com/vmtrace?txhash={}&type=gethtrace2",
        "re": r"<preid=\"editor\"class=\"ms-3\">(.*?)</pre>"
    },
    'heco': {
        "url": "https://www.hecoinfo.com/api/v1/chain/txs/detail?txHash={}&chainId=HECO",
        "re": ""
    },
    'arbi': {
        "url": "https://arbiscan.io/vmtrace?txhash={}&type=gethtrace2",
        "re": r"<preid='editor'>(.*?)</pre>"
    },
    'boba': {
        "url": "https://bobascan.com/vmtrace?txhash={}&type=gethtrace2",
        "re": r"<preid='editor'>(.*?)</pre>"
    },
    'arbi-nova': {
        "url": "https://nova.arbiscan.io/vmtrace?txhash={}&type=gethtrace2",
        "re": r"<preid='editor'>(.*?)</pre>"
    }
}

tenderly_chain_id_list = {
    "arbi": 42161,
    "arbi-testnet": 421613,
    "bsc": 56,
    "bsc-testnet": 97,
    "avax": 43114,
    "avax-testnet": 43113,
    "fantom": 250,
    "ftm-testnet": 25,
    "moonbeam": 1284,
    "moonriver": 1285,
    "cronos": 25,
    "cronos-testnet": 338,
    "boba-testnet": 2888,
    "gnosis": 100,
    "eth": 1,
    "sepolia": 11155111,
    "goerli": 5,
    "poly": 137,
    "poly-testnet": 80001,
    "opt": 10,
    "opt-testnet": 420,
    "base": 8453,
    "base-testnet": 84531,
    "boba": 288
}

special_trace_api = {
    "klaytn": {},
    'ronin': {}
}

chain_to_id = CaseInsensitiveDict({
    "Ethereum Mainnet": 1,
    "Sepolia Testnet": 11155111,
    "Hoodi Testnet": 560048,
    "BNB Smart Chain Mainnet": 56,
    "BNB Smart Chain Testnet": 97,
    "Polygon Mainnet": 137,
    "Polygon Amoy Testnet": 80002,
    "Base Mainnet": 8453,
    "Base Sepolia Testnet": 84532,
    "Arbitrum One Mainnet": 42161,
    "Arbitrum Sepolia Testnet": 421614,
    "Linea Mainnet": 59144,
    "Linea Sepolia Testnet": 59141,
    "Blast Mainnet": 81457,
    "Blast Sepolia Testnet": 168587773,
    "OP Mainnet": 10,
    "OP Sepolia Testnet": 11155420,
    "Avalanche C-Chain": 43114,
    "Avalanche Fuji Testnet": 43113,
    "BitTorrent Chain Mainnet": 199,
    "BitTorrent Chain Testnet": 1029,
    "Celo Mainnet": 42220,
    "Celo Sepolia Testnet": 11142220,
    "Fraxtal Mainnet": 252,
    "Fraxtal Hoodi Testnet": 2523,
    "Gnosis": 100,
    "Mantle Mainnet": 5000,
    "Mantle Sepolia Testnet": 5003,
    "Memecore Mainnet": 4352,
    "Memecore Testnet": 43521,
    "Moonbeam Mainnet": 1284,
    "Moonriver Mainnet": 1285,
    "Moonbase Alpha Testnet": 1287,
    "opBNB Mainnet": 204,
    "opBNB Testnet": 5611,
    "Scroll Mainnet": 534352,
    "Scroll Sepolia Testnet": 534351,
    "Taiko Mainnet": 167000,
    "Taiko Hoodi": 167013,
    "XDC Mainnet": 50,
    "XDC Apothem Testnet": 51,
    "ApeChain Mainnet": 33139,
    "ApeChain Curtis Testnet": 33111,
    "World Mainnet": 480,
    "World Sepolia Testnet": 4801,
    "Sonic Mainnet": 146,
    "Sonic Testnet": 14601,
    "Unichain Mainnet": 130,
    "Unichain Sepolia Testnet": 1301,
    "Abstract Mainnet": 2741,
    "Abstract Sepolia Testnet": 11124,
    "Berachain Mainnet": 80094,
    "Berachain Bepolia Testnet": 80069,
    "Swellchain Mainnet": 1923,
    "Swellchain Testnet": 1924,
    "Monad Mainnet": 143,
    "Monad Testnet": 10143,
    "HyperEVM Mainnet": 999,
    "Katana Mainnet": 747474,
    "Katana Bokuto": 737373,
    "Sei Mainnet": 1329,
    "Sei Testnet": 1328,
    "Stable Mainnet": 988,
    "Stable Testnet": 2201,
    "Plasma Mainnet": 9745,
    "Plasma Testnet": 9746,
    "MegaETH Mainnet": 4326,
    "MegaETH Testnet": 6342,
})

paid_only_chains = [
    "BNB Smart Chain Mainnet",
    "BNB Smart Chain Testnet",
    "Base Mainnet",
    "Base Sepolia Testnet",
    "OP Mainnet",
    "OP Sepolia Testnet",
    "Avalanche C-Chain",
    "Avalanche Fuji Testnet",
]

paid_only_set = {c.lower() for c in paid_only_chains}

chain_id_to_name = {v: k for k, v in chain_to_id.items()}