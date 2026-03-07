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
| `keys.py` | *(已删除)* | 逻辑合并到 `config.py` 的 `get_api_key()` |
| `setup.py` | `pyproject.toml` | 现代化打包方式 |
| *(无)* | `.gitignore` | 新增 |

## 核心改动详解

### 1. 安全：移除硬编码 API Key
- **之前**: `config.py` 中有 7 个 Etherscan API Key 明文写在代码里
- **之后**: `get_api_key()` 按优先级从命令行 → 环境变量 → 配置文件读取
- **用户迁移**: 设置环境变量 `export ETHERSCAN_API_KEY=你的key`，或创建 `~/.getsourcecode/config.json`：
  ```json
  {"api_key": "你的key"}
  ```

### 2. 安全：SSL 验证默认开启
- **之前**: 全局 `verify=False`，所有请求不验证证书
- **之后**: 默认验证证书；如需跳过，使用 `--insecure` 参数
- **用户迁移**: 如果在特殊网络环境下需要跳过验证，加 `--insecure`

### 3. 架构：全局状态 → DownloadContext
- **之前**: `common.py` 中 8 个全局变量，通过 `global` 在多个文件中修改
- **之后**: 所有可变状态封装在 `DownloadContext` 实例中，作为 `ctx` 参数传递
- **好处**: 可测试、无副作用、支持未来并发

### 4. 代码：消除 7 处重复的文件保存逻辑
- **之前**: "检查文件存在 → 重命名 → 去重 → 建目录 → 写文件" 逻辑复制粘贴 7 次
- **之后**: 统一为 `save_contract_file()` 函数
- **每条链的 `send_xxx` 函数从 ~50 行缩减到 ~25 行**

### 5. 依赖：替换废弃库
- `retrying` → `tenacity`（活跃维护）
- `distutils.version.StrictVersion` → 自写 `_parse_version()`（兼容 Python 3.12+）
- 移除无用 import: `from audioop import add`

### 6. 模块加载：无副作用
- **之前**: `import getsourcecode` 会触发 `argparse.parse_args()`
- **之后**: `build_parser()` 只构建 parser，`parse_args()` 在 `main()` 中调用
- **好处**: 可以作为库被其他项目导入

### 7. 日志：print → logging
- 所有 `print()` 替换为 `logging.info/warning/error`
- 异常不再调用 `sys.exit()`，改为 `logger.error` + `continue`
- 批量下载时单个地址失败不会中断整个流程

### 8. 打包：setup.py → pyproject.toml
- 符合 PEP 621 标准
- 依赖声明更清晰
- 移除了 `keys.py`（逻辑合并到 `config.py`）
