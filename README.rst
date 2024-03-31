getSourceCode
=============

This tool is designed to quickly download the code of open source
contracts on the blockchain explorer.

The downloaded code maintains the file directory structure at the time
of verification.

Supported Chain Platforms:

::

    arbi|arbi-nova|avax|base|boba|bsc
    bttc|celo|cronos|eth|fantom|gnosis
    heco|klaytn|linea|moonbeam|moonriver
    okt|opt|poly|poly-zk|ronin|tron|zkSyncEra

    alfajores|arbi-testnet|avax-testnet
    baobab|base-testnet|boba-testnet|bsc-testnet
    bttc-testnet|ftm-testnet|goerli|heco-testnet
    linea-testnet|moonbase|opt-testnet|okb
    okt-testnet|opBNB|poly-testnet|poly-zk-testnet
    ronin-testnet|sepolia|zkSyncEra-testnet



Get code by tx only supports:

::

    arbi|arbi-nova|avax|base|boba|bsc
    cronos|eth|fantom|gnosis|heco|klaytn
    moonbeam|moonriver|opt|poly||ronin

    arbi-testnet|avax-testnet|base-testnet
    boba-testnet|bsc-testnet|ftm-testnet
    goerli|opt-testnet|poly-testnet



Install
=======

::

   pip install getSourceCode

Usage
=====

::

   getCode [-h] [-i INPUTFILE] [-o OUTPUTFOLDER] [-a ADDRESS] [-n NETWORK] [-k] [-p PROXY] [-t TXHASH] [-u] [-v] [--apikey APIKEY]

For example:

::

   getCode -n bsc -a 0xb51eaa437AC67A631e2FEca0a18dA7a6391c0D07

or

::

   getCode -n eth -a 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 -p 127.0.0.1:7890

The command execution result is as follows:

::

    [root@hxzy test]# getCode -n bsc -a 0xb51eaa437AC67A631e2FEca0a18dA7a6391c0D07
    0-0: SynthereumManager/deploy/@openzeppelin/contracts/access/AccessControl.sol
    0-1: SynthereumManager/deploy/@openzeppelin/contracts/access/IAccessControl.sol
    0-2: SynthereumManager/deploy/@openzeppelin/contracts/utils/Context.sol
    0-3: SynthereumManager/deploy/@openzeppelin/contracts/utils/Strings.sol
    0-4: SynthereumManager/deploy/@openzeppelin/contracts/utils/introspection/ERC165.sol
    0-5: SynthereumManager/deploy/@openzeppelin/contracts/utils/introspection/IERC165.sol
    0-6: SynthereumManager/deploy/@openzeppelin/contracts/access/AccessControlEnumerable.sol
    0-7: SynthereumManager/deploy/@openzeppelin/contracts/access/IAccessControlEnumerable.sol
    0-8: SynthereumManager/deploy/@openzeppelin/contracts/utils/structs/EnumerableSet.sol
    0-9: SynthereumManager/deploy/contracts/core/Manager.sol
    0-10: SynthereumManager/deploy/contracts/core/interfaces/IFinder.sol
    0-11: SynthereumManager/deploy/contracts/core/interfaces/IManager.sol
    0-12: SynthereumManager/deploy/contracts/common/interfaces/IEmergencyShutdown.sol
    0-13: SynthereumManager/deploy/contracts/core/Constants.sol
    0-14: SynthereumManager/deploy/contracts/core/Finder.sol

    Address => ContractName:
    0xb51eaa437AC67A631e2FEca0a18dA7a6391c0D07      SynthereumManager

    Success.

The directory structure looks like this:

::

    [root@hxzy test]# tree
    .
    └── SynthereumManager
        └── deploy
            ├── contracts
            │   ├── common
            │   │   └── interfaces
            │   │       └── IEmergencyShutdown.sol
            │   └── core
            │       ├── Constants.sol
            │       ├── Finder.sol
            │       ├── interfaces
            │       │   ├── IFinder.sol
            │       │   └── IManager.sol
            │       └── Manager.sol
            └── @openzeppelin
                └── contracts
                    ├── access
                    │   ├── AccessControlEnumerable.sol
                    │   ├── AccessControl.sol
                    │   ├── IAccessControlEnumerable.sol
                    │   └── IAccessControl.sol
                    └── utils
                        ├── Context.sol
                        ├── introspection
                        │   ├── ERC165.sol
                        │   └── IERC165.sol
                        ├── Strings.sol
                        └── structs
                            └── EnumerableSet.sol

    13 directories, 15 files

Get code by tx only:

::

    getCode -n eth -t 0x8dda3f4a1c4bbc85ed50d7a78096f805f2c9382e35800e42f066abaa7b17a71b -p 127.0.0.1:7890

The address without the corresponding contract name is an unopened contract\EOA.

Like this:

::

    [root@hxzy test]#getCode -n eth -t 0x8dda3f4a1c4bbc85ed50d7a78096f805f2c9382e35800e42f066abaa7b17a71b -p 127.0.0.1:7890
    0-0: contract/AnyswapV6ERC20.sol
    1-0: contract/FiatTokenProxy.sol
    2-0: Implementation/FiatTokenV2_1.sol
    3-0: contract/AnyswapV6Router.sol
    4-0: contract/FiatTokenV2_1.sol

    Address => ContractName:
    0xea928a8d09e11c66e074fbf2f6804e19821f438d      AnyswapV6ERC20
    0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48      FiatTokenProxy
    0xa2327a938febf5fec13bacfb16ae10ecbc4cbdcf      FiatTokenV2_1
    0x7782046601e7b9b05ca55a3899780ce6ee6b8b2b      AnyswapV6Router
    0xe19105463d6fe2f2bd86c69ad478f4b76ce49c53

    Proxy => Implementation:
    0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48      0xa2327a938febf5fec13bacfb16ae10ecbc4cbdcf

    Success.

If there is a proxy contract, it will be displayed like this:

::

    Proxy => Implementation:
    0xff970a61a04b1ca14834a43f5de4533ebddb5cc8      0x1efb3f88bc88f03fd1804a5c53b7141bbef5ded8
    0x82af49447d8a07e3bd95bd0d56f35241523fbab1      0x8b194beae1d3e0788a1a35173978001acdfba668


In particular, the okex related chain needs apikey to use.


::

    [root@hxzy test]#getCode -n okt -p 127.0.0.1:7890 -a 0x0eC4020F29faa430754f1dB07B66798d31006771
    If you want to get the contract code of the okex link, you need to manually enter the api key.
    Visit this link:
    1. okt: https://www.oklink.com/cn/oktc/address/0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE
    2. okb: https://www.oklink.com/cn/okbc-test/address/0x6BC26C28130e7634fFa1330969f34e98DC4d0019
    3. okt-testnet: https://www.oklink.com/cn/oktc-test/address/0x7c3ebCB6c4Ae99964980006C61d7eb032eDcb06B

    Follow the steps below:
    1. Open the above link
    2. Open the browser developer tool
    3. Click the contract tab page on the browser
    4. Find the request "contract?t="
    5. X-Apikey in the request header of the request is the required apikey

    For example:
    getCode -p 127.0.0.1:7890 -n okt -a 0x38AB5022BEa07AA8966A9bEB5EF7759b715e4BEE --apikey LWIzMWUtNDU0Ny05Mjk5LWI2ZDA3Yjc2MzFhYmEyYzkwM2NjfDI4MDQzNDU3Mjc2NjY0OTI=

Parameter description:

::

    optional arguments:
    -h, --help       show this help message and exit
    -i INPUTFILE     Input file path including contract addresses.
    -o OUTPUTFOLDER  Choose a folder to export.
    -a ADDRESS       A string including contract addresses.
    -n NETWORK       Which network to get source code.
    -k               Provide some blockchain explorer api keys.
    -p PROXY         Use a proxy.
    -t TXHASH        Get the relevant contract source code in the specified transaction.
    -u               Check to see if a new version is available to update.
    -v               Show version
    --apikey APIKEY  The apikey required by the okex related chain.


Contact
=======

If you have any suggestions or needs please contact: support@hxzy.me

Github: https://github.com/5hawnXu/getSourceCode