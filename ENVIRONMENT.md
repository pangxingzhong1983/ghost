## 环境概览

- **来源**：`README.md` 的 Development Install 段落说明（ghost/README.md:11-38）+ 本次在 macOS 13 arm64 上的实际验证日志。
- **目标**：确保仓库内始终有可复用的 Python3.9 虚拟环境 `ghostvenv`，避免重复搭建。

## 系统依赖

| 依赖 | 版本/命令 | 备注 |
| --- | --- | --- |
| Python | 3.9.x | macOS 自带，可用 `python3 --version` 验证 |
| Homebrew | 任意可用版本 | 用于安装构建依赖 |
| swig | `brew install swig` | 供 `M2Crypto` 构建使用 |
| openssl@1.1 | `brew install openssl@1.1` | 需配合编译参数 |

> 安装 openssl@1.1 后，若未写入 shell rc，可在执行 pip 前导出：
> `export CFLAGS='-I/opt/homebrew/opt/openssl@1.1/include'`
> `export CPPFLAGS='-I/opt/homebrew/opt/openssl@1.1/include'`
> `export LDFLAGS='-L/opt/homebrew/opt/openssl@1.1/lib'`
> `export PKG_CONFIG_PATH='/opt/homebrew/opt/openssl@1.1/lib/pkgconfig'`
> `export SWIG_FEATURES='-I/opt/homebrew/opt/openssl@1.1/include'`

## 虚拟环境创建/使用

```bash
cd /Users/pangxingzhong/workspace/ghost
python3 -m venv ghostvenv
source ghostvenv/bin/activate
```

> 当前虚拟环境存放位置：`ghost/ghostvenv`

## 依赖安装流程

1. 激活虚拟环境并导出上节中的 OpenSSL 相关环境变量。
2. 安装 `pip` 最新版（`python -m pip install --upgrade pip`），否则某些 wheel 会触发旧版 bug。
3. 先单独安装难构建的依赖：
   ```bash
   pip install M2Crypto==0.46.2
   ```
4. 处理 `pylzma==0.5.0` 的 Python 3.8+ 兼容性问题（详见下节）。
5. 执行常规依赖安装：
   ```bash
   pip install -r requirements.txt
   ```

完成后即可运行：

```bash
source ghostvenv/bin/activate
python -m ghost.cli --help
```

首次运行会提示 `urllib3` 因系统 LibreSSL 触发的 Warning，可忽略或切换到官方 OpenSSL 构建的 Python。

## pylzma 补丁

`pylzma 0.5.0` 在 Python 3.9 上使用遗留的 `tp_print` 槽会导致编译错误。处理方式：

1. 下载源码包并解压：
   ```bash
   pip download pylzma==0.5.0
   tar -xf pylzma-0.5.0.tar.gz
   ```
2. 将以下文件中 `NULL /* printfunc tp_print */` 手动改为 `0`：
   - `src/pylzma/pylzma_compressobj.c`
   - `src/pylzma/pylzma_compressfile.c`
   - `src/pylzma/pylzma_aes.c`
   - `src/pylzma/pylzma_decompressobj.c`
   - `src/pylzma/pylzma_decompressobj_compat.c`
3. 使用修改后的源码安装：
   ```bash
   pip install ./pylzma-0.5.0
   ```
4. 清理临时目录即可。

> 该补丁消除了 `clang` 报错的 `Py_ssize_t` 类型不匹配问题；如后续官方发布新版本，可移除手动步骤。

## 运行提醒

- 每次执行 `pip install`、`python -m ghost.cli` 等命令前，请确认 `ghostvenv` 已激活。
- 若需重建环境，只需删除旧虚拟环境目录 `rm -rf ghostvenv` 并重复本文步骤。
