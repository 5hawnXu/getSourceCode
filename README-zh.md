# getSourceCode

本工具用于快速下载区块链浏览器上开源合约的代码，下载的代码会保留验证时的文件目录结构。

支持的链平台：

    Ethereum Mainnet | Sepolia Testnet | Hoodi Testnet
    BNB Smart Chain Mainnet | BNB Smart Chain Testnet
    Polygon Mainnet | Polygon Amoy Testnet
    Base Mainnet | Base Sepolia Testnet
    Arbitrum One Mainnet | Arbitrum Sepolia Testnet
    Linea Mainnet | Linea Sepolia Testnet
    Blast Mainnet | Blast Sepolia Testnet
    OP Mainnet | OP Sepolia Testnet
    Avalanche C-Chain | Avalanche Fuji Testnet
    BitTorrent Chain Mainnet | BitTorrent Chain Testnet
    Celo Mainnet | Celo Sepolia Testnet
    Fraxtal Mainnet | Fraxtal Hoodi Testnet
    Gnosis...

> ⚠️ 链名不区分大小写。

> ⚠️ 部分链（如 BNB Smart Chain、Base、OP、Avalanche）需要付费 API 套餐。

> 完整支持列表请访问：https://docs.etherscan.io/supported-chains

仅支持通过交易哈希获取合约代码的链：

    arbi|arbi-nova|avax|base|boba|bsc
    cronos|eth|fantom|gnosis|heco|klaytn
    moonbeam|moonriver|opt|poly|ronin

    arbi-testnet|avax-testnet|base-testnet
    boba-testnet|bsc-testnet|ftm-testnet
    goerli|opt-testnet|poly-testnet

# 安装

    pip install getSourceCode

# 使用方法

    getCode [-h] [-i 输入文件] [-o 输出目录] [-a 合约地址] [-n 网络] [-k 密钥] [-p 代理] [-t 交易哈希] [-u] [-v] [--apikey API密钥]

示例：

    getCode -n "Ethereum Mainnet" -a 0xb51eaa437AC67A631e2FEca0a18dA7a6391c0D07

或使用代理：

    getCode -n "Ethereum Mainnet" -a 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 -p 127.0.0.1:7890

执行结果如下：

    [root@hxzy test]# getCode -n "Ethereum Mainnet" -a 0xb51eaa437AC67A631e2FEca0a18dA7a6391c0D07
    0-0: SynthereumManager/deploy/@openzeppelin/contracts/access/AccessControl.sol
    0-1: SynthereumManager/deploy/@openzeppelin/contracts/access/IAccessControl.sol
    ...（省略）
    0-14: SynthereumManager/deploy/contracts/core/Finder.sol

    Address => ContractName:
    0xb51eaa437AC67A631e2FEca0a18dA7a6391c0D07      SynthereumManager

    Success.

目录结构如下：

    [root@hxzy test]# tree
    .
    └── SynthereumManager
        └── deploy
            ├── contracts
            │   ├── common
            │   │   └── interfaces
            │   │       └── IEmergencyShutdown.sol
            │   └── core
            │       ├── Constants.sol
            │       ├── Finder.sol
            │       ├── interfaces
            │       │   ├── IFinder.sol
            │       │   └── IManager.sol
            │       └── Manager.sol
            └── @openzeppelin
                └── contracts
                    ├── access
                    │   ├── AccessControlEnumerable.sol
                    │   ├── AccessControl.sol
                    │   ├── IAccessControlEnumerable.sol
                    │   └── IAccessControl.sol
                    └── utils
                        ├── Context.sol
                        ├── introspection
                        │   ├── ERC165.sol
                        │   └── IERC165.sol
                        ├── Strings.sol
                        └── structs
                            └── EnumerableSet.sol

    13 directories, 15 files

通过交易哈希获取合约代码：

    getCode -n "Ethereum Mainnet" -t 0x8dda3f4a1c4bbc85ed50d7a78096f805f2c9382e35800e42f066abaa7b17a71b -p 127.0.0.1:7890

没有对应合约名称的地址为未开源合约或 EOA 账户，示例如下：

    Address => ContractName:
    0xea928a8d09e11c66e074fbf2f6804e19821f438d      AnyswapV6ERC20
    ...
    0xe19105463d6fe2f2bd86c69ad478f4b76ce49c53

若存在代理合约，将额外显示代理与实现的对应关系：

    Proxy => Implementation:
    0xff970a61a04b1ca14834a43f5de4533ebddb5cc8      0x1efb3f88bc88f03fd1804a5c53b7141bbef5ded8
    0x82af49447d8a07e3bd95bd0d56f35241523fbab1      0x8b194beae1d3e0788a1a35173978001acdfba668

## OKEx 相关链

OKEx 相关链（okt / okb / okt-testnet）需要手动提供 apikey，获取方式如下：

1. 在浏览器中打开对应地址页面（示例链接见下方）
2. 打开浏览器开发者工具
3. 点击合约选项卡
4. 找到 `contract?t=` 开头的请求
5. 请求头中的 `X-Apikey` 即为所需的 apikey

对应链的示例链接：
- okt：https://www.oklink.com/cn/oktc/address/0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE
- okb：https://www.oklink.com/cn/okbc-test/address/0x6BC26C28130e7634fFa1330969f34e98DC4d0019
- okt-testnet：https://www.oklink.com/cn/oktc-test/address/0x7c3ebCB6c4Ae99964980006C61d7eb032eDcb06B

获取 apikey 后使用示例：

    getCode -p 127.0.0.1:7890 -n okt -a 0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE --apikey LWIzMWUtNDU0Ny05Mjk5LWI2ZDA3Yjc2MzFhYmEyYzkwM2NjfDI4MDQzNDU3Mjc2NjY0OTI=

# 参数说明

    可选参数：
    -h, --help       显示帮助信息并退出
    -i INPUTFILE     包含合约地址的输入文件路径
    -o OUTPUTFOLDER  指定导出目录
    -a ADDRESS       合约地址字符串
    -n NETWORK       指定获取源码的网络
    -k KEY           提供付费 API Key 以下载付费网络的合约代码
    -p PROXY         使用代理
    -t TXHASH        获取指定交易中涉及的合约源码
    -u               检查是否有新版本可更新
    -v               显示版本号
    --apikey APIKEY  OKEx 相关链所需的 apikey

# 联系方式

如有建议或需求，请联系：<support@hxzy.me>