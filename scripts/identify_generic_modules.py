#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
识别真正跨平台但未声明 darwin 的模块
策略：
1) 优先：无 compatibilities 声明（默认全平台可用）→ 可显式加上 darwin 以标记支持
2) 次选：compatibilities 包含 'posix' 或 'linux' 且未包含 'darwin'，同时代码中未出现 windows 专有库（winreg, pywin32, ctypes.windll, subprocess.CREATE_NEW_CONSOLE 等）
"""

import os
import re

MODULES_DIR = os.path.join(os.path.dirname(__file__), '..', 'ghost', 'modules')
MODULES_DIR = os.path.abspath(MODULES_DIR)

def get_config_info(fp):
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    m = re.search(r'@config\([^)]+\)', txt, re.DOTALL)
    config_block = m.group(0) if m else ''
    # 提取 compatibilities 列表
    compat_match = re.search(r'compatibilities=\[(.*?)\]', config_block, re.DOTALL)
    platforms = []
    if compat_match:
        try:
            platforms = eval('[' + compat_match.group(1) + ']')
        except:
            pass
    return config_block, platforms, txt

def is_windows_specific(txt):
    windows_indicators = [
        'import winreg',
        'import win32',
        'ctypes.windll',
        'subprocess.CREATE_NEW_CONSOLE',
        'win32api',
        'win32con',
        'win32security',
        'pywintypes',
        'win32process',
        'win32event',
        'win32service',
        'wintypes',
        'GetLastError',
        'kernel32',
        'advapi32',
        'USER32',
    ]
    for ind in windows_indicators:
        if ind in txt:
            return True
    return False

def main():
    to_add_darwin = []
    for fn in os.listdir(MODULES_DIR):
        if not fn.endswith('.py') or fn == '__init__.py':
            continue
        fp = os.path.join(MODULES_DIR, fn)
        config_block, platforms, txt = get_config_info(fp)
        # 如果已经有 darwin，跳过
        if 'darwin' in platforms:
            continue
        # 如果包含 windows 专用特征，跳过
        if is_windows_specific(txt):
            continue
        # 如果 compatibilities 为空，或包含 posix/linux/windows 但无 darwin，认为可以加 darwin
        # 但 windows 专用的仍跳过（通过前面 windows_specific 判断），这里 platforms 含 windows 也可能是跨平台混合（如用条件分支），但为保险，我们仅处理以下情况：
        # - platforms 为空（全平台）
        # - platforms 仅含 'posix' 或 'linux' 且不含 'windows'
        # - platforms 含 'windows' 但代码不含 windows 专用特征（即实际跨平台），也可考虑，但需人工确认
        if not platforms:
            to_add_darwin.append((fn, 'no_compat_block'))
        elif set(platforms) <= {'posix', 'linux'}:
            to_add_darwin.append((fn, 'posix_family'))
        elif 'windows' in platforms and not is_windows_specific(txt):
            to_add_darwin.append((fn, 'windows_but_generic'))
        # else: skip
    print(f"=== 可添加 darwin 支持的模块 ({len(to_add_darwin)}) ===")
    for fn, reason in to_add_darwin:
        print(f"{fn}  # {reason}")
    # 生成候选列表文件
    out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'generic_modules_without_darwin.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        import json
        json.dump([{'file': fn, 'reason': reason} for fn, reason in to_add_darwin], f, indent=2, ensure_ascii=False)
    print(f"\n候选列表已保存：{out_path}")

if __name__ == '__main__':
    main()
