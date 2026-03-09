# v3.0.1 变更说明

### 1. 修复：多文件下载时文件名损坏
- **问题**: 下载多个合约时，路径中含 `_` 的文件（如 `node_modules/...`）在冲突重命名时被截断为 `node_0.sol`
- **原因**: `save_contract_file()` 中对整个路径执行 `split('_')[0]`，破坏了目录结构
- **修复**: 使用 `os.path.dirname` + `os.path.basename` + `os.path.splitext` 正确分离目录与文件名，仅对文件名部分追加索引后缀

### 2. 新功能：`--chainid` 参数
- 支持通过链 ID 直接指定网络，无需输入完整链名
- 示例: `getCode --chainid 1 -a 0x1234...` 等同于 `getCode -n "Ethereum Mainnet" -a 0x1234...`
- 已知链 ID 自动解析为链名；未知链 ID 直接传递给 etherscan v2 API

### 3. 优化：实现合约保存到代理合约子目录
- **之前**: 所有实现合约保存在同一个 `Implementation/` 目录，多个代理合约的实现混在一起
- **之后**: 实现合约保存到 `{代理合约名}/Implementation/` 子目录下
- 同时修复了 `send_okex` 中 `impl_contract` 硬编码目录名不一致的问题

### 4. 优化：同名合约自动去重文件夹
- **问题**: 多个代理合约同名（如都叫 `ERC1967Proxy`）时文件夹冲突
- **修复**: 新增 `get_unique_contract_folder()` 函数，检测同批次内是否有其他地址使用相同合约名，自动追加地址前缀区分（如 `ERC1967Proxy_0xfa8C`）

---

# v3.0.0 重构变更说明

## 文件对照表

| 原文件 | 新文件 | 主要变化 |
|--------|--------|----------|
| `__init__.py` | `__init__.py` | argparse 移入 `main()`；消除模块加载副作用 |
| `common.py` | `common.py` | 全局变量 → `DownloadContext` 类；新增 `save_contract_file()` |
| `config.py` | `config.py` | 删除硬编码 API Key；新增 `get_api_key()` 多来源读取 |
| `handle.py` | `handle.py` | 消除 7 处重复代码；移除 `global`；传入 `ctx` |
| `filter.py` | `filter.py` | 显式导入；传入 `ctx`；更清晰的函数拆分 |
| `check.py` | `check.py` | 用自写 `_parse_version()` 替代废弃的 `distutils` |
| `menu.py` | `menu.py` | `argparse_menu()` → `build_parser()`，不再自动 `parse_args()` |
| `setup.py` | `pyproject.toml` | 现代化打包方式 |
| *(无)* | `.gitignore` | 新增 |

## 核心改动详解

### 1. 架构：全局状态 → DownloadContext
- **之前**: `common.py` 中 8 个全局变量，通过 `global` 在多个文件中修改
- **之后**: 所有可变状态封装在 `DownloadContext` 实例中，作为 `ctx` 参数传递
- **好处**: 可测试、无副作用、支持未来并发

### 2. 代码：消除 7 处重复的文件保存逻辑
- **之前**: "检查文件存在 → 重命名 → 去重 → 建目录 → 写文件" 逻辑复制粘贴 7 次
- **之后**: 统一为 `save_contract_file()` 函数
- **每条链的 `send_xxx` 函数从 ~50 行缩减到 ~25 行**

### 3. 依赖：替换废弃库
- `retrying` → `tenacity`（活跃维护）
- `distutils.version.StrictVersion` → 自写 `_parse_version()`（兼容 Python 3.12+）
- 移除无用 import: `from audioop import add`

### 4. 模块加载：无副作用
- **之前**: `import getsourcecode` 会触发 `argparse.parse_args()`
- **之后**: `build_parser()` 只构建 parser，`parse_args()` 在 `main()` 中调用
- **好处**: 可以作为库被其他项目导入

