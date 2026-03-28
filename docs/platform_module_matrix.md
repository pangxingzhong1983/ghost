# Ghost 模块平台支持矩阵

> 生成时间：2026-03-28
> 数据源：`python3 scripts/analyze_module_platforms.py`

## 覆盖统计（按显式 `compatibilities` 声明）

| platform | module count |
|---|---:|
| darwin | 7 |
| linux | 8 |
| posix | 2 |
| solaris | 1 |
| windows | 10 |

- 模块总数：122
- 显式声明 darwin：7
- 未显式声明 darwin：115

## 当前显式支持 darwin 的模块

- `check_vm.py`
- `creddump.py`
- `drives.py`
- `msgbox.py`
- `rdp.py`
- `screenshot.py`
- `users.py`

## 说明

1. 这里统计的是**显式声明**，不是“理论可运行”总数。很多通用模块没有写 `compatibilities`，仍可能可运行。
2. 若要做“全功能工程版”，建议先做三件事：
   - 自动生成并持续维护平台矩阵（已完成）
   - 在模块加载时做平台兼容性硬检查并返回可读错误（已完成）
   - 分批把通用模块补上显式平台声明（待执行）

## 可复现命令

```bash
cd /Users/pangxingzhong/.openclaw/workspace/Ghost
python3 scripts/analyze_module_platforms.py
python3 scripts/identify_generic_modules.py
```
