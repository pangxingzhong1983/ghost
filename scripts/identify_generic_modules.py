#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
识别可能补充 darwin 显式声明的模块候选。

策略：
1. 无平台声明：仅代表边界未写清，列为 no_compat_block
2. 仅 posix/linux：列为 posix_family
3. 显式含 windows 但源码无明显 Windows 专属特征：列为 windows_but_generic
"""

from __future__ import annotations

import json
import os

from analyze_module_platforms import DOCS_DIR, MODULES_DIR, load_modules


WINDOWS_INDICATORS = (
    "import winreg",
    "import win32",
    "ctypes.windll",
    "subprocess.CREATE_NEW_CONSOLE",
    "win32api",
    "win32con",
    "win32security",
    "pywintypes",
    "win32process",
    "win32event",
    "win32service",
    "wintypes",
    "GetLastError",
    "kernel32",
    "advapi32",
    "USER32",
    "pupwinutils.",
)


def is_windows_specific(source):
    return any(indicator in source for indicator in WINDOWS_INDICATORS)


def read_source(filename):
    filepath = os.path.join(MODULES_DIR, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def main():
    candidates = []

    for module in load_modules():
        platforms = set(module["platforms"])
        if "darwin" in platforms:
            continue

        source = read_source(module["file"])
        windows_specific = is_windows_specific(source)

        if not platforms:
            candidates.append((module["file"], "no_compat_block"))
        elif platforms <= {"posix", "linux"}:
            candidates.append((module["file"], "posix_family"))
        elif (
            "windows" in platforms and
            "android" not in platforms and
            not windows_specific
        ):
            candidates.append((module["file"], "windows_but_generic"))

    candidates.sort()

    print("=== 可添加 darwin 支持的模块 ({}) ===".format(len(candidates)))
    for filename, reason in candidates:
        print("{}  # {}".format(filename, reason))

    out_path = os.path.join(DOCS_DIR, "generic_modules_without_darwin.json")
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(
            [{"file": filename, "reason": reason} for filename, reason in candidates],
            handle,
            indent=2,
            ensure_ascii=False,
        )
        handle.write("\n")

    print("\n候选列表已保存：{}".format(out_path))


if __name__ == "__main__":
    main()
