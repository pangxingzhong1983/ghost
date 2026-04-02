# Ghost Platform Matrix Refresh (2026-03-28)

## 1) 用户需求 / 任务目的 / 背景
- 需求：基于当前仓库状态，生成一份可靠的 Ghost 平台能力矩阵，明确 Android / macOS / Linux / Windows 的显式模块覆盖情况。
- 背景：仓库内已经存在 `docs/platform_module_matrix.md`、`docs/module_platform_report.json` 和对应脚本，但统计值明显过期，与当前源码不一致。

## 2) 本次所有变更点
- 重写 `scripts/analyze_module_platforms.py` 的兼容声明解析逻辑，支持 `@config(compat=...)`、`compatibility=...`、`compatibilities=...` 三种字段。
- 支持同时解析字符串写法与列表写法，例如 `compat="windows"`、`compat=["android"]`、`compatibilities=['windows', 'linux']`。
- 分析脚本改为同时输出：
  - `docs/module_platform_report.json`
  - `docs/platform_module_matrix.md`
- 新增平台分类分布统计与“未显式声明平台模块”清单。
- 修正 `scripts/identify_generic_modules.py`，改为复用新的模块解析结果，避免把 Android-only / Windows-only 模块误判成可补 darwin。
- 重新生成：
  - `docs/module_platform_report.json`
  - `docs/platform_module_matrix.md`
  - `docs/generic_modules_without_darwin.json`

## 3) 变更前后差异对照

### 旧结果
- `docs/platform_module_matrix.md` 统计为：
  - 模块总数 `122`
  - `darwin 7`
  - `linux 8`
  - `windows 10`
  - 无 `android` 行
- 根因：`scripts/analyze_module_platforms.py` 只匹配 `compatibilities=[...]`，漏掉仓库中大量实际使用的 `compat=` 与字符串形式。

### 新结果
- 当前重生成后的矩阵统计为：
  - 模块总数 `122`
  - `windows 46`
  - `linux 32`
  - `darwin 11`
  - `android 7`
  - `posix 5`
  - `solaris 3`
  - `all 1`
- Android 当前显式模块仅为：
  - `apps.py`
  - `call.py`
  - `contacts.py`
  - `gpstracker.py`
  - `text_to_speach.py`
  - `vibrate.py`
  - `webcamsnap.py`
- macOS 当前显式模块为：
  - `check_vm.py`
  - `creddump.py`
  - `drives.py`
  - `keylogger.py`
  - `lock_screen.py`
  - `msgbox.py`
  - `rdesktop.py`
  - `rdp.py`
  - `screenshot.py`
  - `sudo_alias.py`
  - `users.py`

## 4) 使用方式 / 依赖 / 注意事项
- 在 Ghost 仓库根目录执行：

```bash
cd /Users/pangxingzhong/.openclaw/workspace/Ghost
python3 scripts/analyze_module_platforms.py
python3 scripts/identify_generic_modules.py
```

- `analyze_module_platforms.py` 会覆盖生成最新的 JSON 报告与 Markdown 矩阵。
- `identify_generic_modules.py` 会输出候选清单到 `docs/generic_modules_without_darwin.json`。
- 这两份结果都是“显式声明”视角，不等于所有模块都已经真实跨平台验证通过。

## 5) 风险点与回滚方案
- 风险：
  - 本次修正的是统计与文档链路，不是运行时模块实现；矩阵变准了，不代表模块本身新增了平台能力。
  - 仍有 `58` 个模块未显式声明平台，后续若仅凭“无声明”就推断可跨平台，仍有误判风险。
- 回滚：
  - 回退以下文件即可恢复到修正前状态：
    - `scripts/analyze_module_platforms.py`
    - `scripts/identify_generic_modules.py`
    - `docs/module_platform_report.json`
    - `docs/platform_module_matrix.md`
    - `docs/generic_modules_without_darwin.json`

## 6) 后续可扩展与优化建议
- 继续给未声明平台的通用模块补显式 `compat` 标签，减少灰区。
- 为 `docs/platform_module_matrix.md` 增加“高风险能力”分层，例如 `creds / privesc / exploit / pivot`。
- 在 CI 中增加断言，防止矩阵脚本回退成旧解析逻辑后又产出错误统计。

## 7) 记忆更新
- 本次结论适合沉淀为项目记忆：Ghost 的平台矩阵脚本曾因只识别 `compatibilities=[...]` 而低估 Android/macOS/Windows/Linux 的实际显式覆盖数，后续应统一复用 AST 解析结果，避免统计链路与候选链路漂移。
