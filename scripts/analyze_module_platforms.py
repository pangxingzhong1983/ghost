#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ghost 模块平台覆盖分析器

扫描 ghost/modules 下所有顶层模块，提取 @config() 中的：
- compat
- compatibility
- compatibilities

同时生成：
- docs/module_platform_report.json
- docs/platform_module_matrix.md
"""

from __future__ import annotations

import ast
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES_DIR = os.path.join(ROOT_DIR, "ghost", "modules")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
REPORT_PATH = os.path.join(DOCS_DIR, "module_platform_report.json")
MATRIX_PATH = os.path.join(DOCS_DIR, "platform_module_matrix.md")
SUPPORTED_PLATFORMS = ("windows", "linux", "darwin", "android", "posix", "solaris", "all")


def normalize_platform(value):
    value = str(value).strip().lower()

    if "darwin" in value or "osx" in value or value == "mac":
        return "darwin"
    if "android" in value:
        return "android"
    if "linux" in value:
        return "linux"
    if "win" in value:
        return "windows"
    if "solaris" in value:
        return "solaris"
    if "posix" in value:
        return "posix"
    if value == "all":
        return "all"

    return value


def literal_value(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def parse_module(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as handle:
        source = handle.read()

    tree = ast.parse(source, filepath)

    class_name = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__class_name__":
                    class_name = literal_value(node.value)
                    break
        if class_name:
            break

    compat = []
    category = None
    decorated_class = None

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            if not isinstance(decorator.func, ast.Name) or decorator.func.id != "config":
                continue

            decorated_class = node.name
            kwargs = {
                keyword.arg: keyword.value
                for keyword in decorator.keywords
                if keyword.arg
            }

            for key in ("category", "cat"):
                if key in kwargs:
                    category = literal_value(kwargs[key])
                    break

            raw_compat = None
            for key in ("compatibilities", "compatibility", "compat"):
                if key in kwargs:
                    raw_compat = literal_value(kwargs[key])
                    break

            if isinstance(raw_compat, str):
                compat = [raw_compat]
            elif isinstance(raw_compat, (list, tuple, set)):
                compat = list(raw_compat)
            else:
                compat = []

            break

        if decorated_class:
            break

    compatible_systems = sorted(
        {
            normalize_platform(item)
            for item in compat
            if normalize_platform(item)
        }
    )

    return {
        "file": os.path.basename(filepath),
        "class_name": class_name or decorated_class,
        "category": category,
        "platforms": compatible_systems,
    }


def load_modules():
    modules = []

    for filename in sorted(os.listdir(MODULES_DIR)):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        filepath = os.path.join(MODULES_DIR, filename)
        modules.append(parse_module(filepath))

    return modules


def build_report(modules):
    coverage = Counter()
    category_by_platform = defaultdict(Counter)
    platform_modules = defaultdict(list)

    for module in modules:
        for platform in module["platforms"]:
            coverage[platform] += 1
            category = module["category"] or "unknown"
            category_by_platform[platform][category] += 1
            platform_modules[platform].append(module["file"])

    for platform in platform_modules:
        platform_modules[platform].sort()

    missing = {
        platform: sorted(
            module["file"]
            for module in modules
            if platform not in module["platforms"]
        )
        for platform in ("darwin", "linux", "android", "windows")
    }

    unspecified = sorted(
        module["file"]
        for module in modules
        if not module["platforms"]
    )

    quick_win_candidates = sorted(
        module["file"]
        for module in modules
        if not module["platforms"] or (
            "windows" in module["platforms"] and "darwin" not in module["platforms"]
        )
    )

    generated_at = datetime.now().isoformat(timespec="seconds")

    return {
        "generated_at": generated_at,
        "module_total": len(modules),
        "coverage": {platform: coverage[platform] for platform in sorted(coverage)},
        "category_by_platform": {
            platform: dict(sorted(categories.items()))
            for platform, categories in sorted(category_by_platform.items())
        },
        "platform_modules": {
            platform: files
            for platform, files in sorted(platform_modules.items())
        },
        "all_modules": modules,
        "missing_darwin": missing["darwin"],
        "missing_linux": missing["linux"],
        "missing_android": missing["android"],
        "missing_windows": missing["windows"],
        "unspecified": unspecified,
        "quick_win_candidates": quick_win_candidates,
    }


def build_markdown(report):
    coverage_order = ["windows", "linux", "darwin", "android", "posix", "solaris", "all"]

    lines = [
        "# Ghost 模块平台支持矩阵",
        "",
        "> 生成时间：{}".format(report["generated_at"]),
        "> 数据源：`python3 scripts/analyze_module_platforms.py`",
        "",
        "## 覆盖统计（按显式 `@config` 声明）",
        "",
        "| platform | module count |",
        "|---|---:|",
    ]

    for platform in coverage_order:
        count = report["coverage"].get(platform)
        if count:
            lines.append("| {} | {} |".format(platform, count))

    lines.extend([
        "",
        "- 模块总数：{}".format(report["module_total"]),
        "- 未显式声明平台：{}".format(len(report["unspecified"])),
        "- 显式支持 darwin：{}".format(report["coverage"].get("darwin", 0)),
        "- 显式支持 android：{}".format(report["coverage"].get("android", 0)),
        "",
        "## 能力缺口速览",
        "",
        "- Windows：显式模块最多，且包含 `privesc`/`exploit` 能力。",
        "- Linux：覆盖面次之，包含少量 `privesc`/`exploit` 能力。",
        "- macOS：显式模块较少，当前无显式 `privesc`/`exploit` 模块。",
        "- Android：当前显式模块仅覆盖 `gather` 与 `troll`，没有显式 `creds`/`privesc`/`exploit` 模块。",
        "",
        "## 各平台显式模块清单",
        "",
    ])

    for platform in ("windows", "linux", "darwin", "android"):
        files = report["platform_modules"].get(platform, [])
        categories = report["category_by_platform"].get(platform, {})
        category_text = ", ".join(
            "{}={}".format(name, value)
            for name, value in sorted(categories.items())
        ) or "无"

        lines.extend([
            "### {} ({})".format(platform, len(files)),
            "",
            "- 分类分布：{}".format(category_text),
        ])

        if files:
            lines.extend("- `{}`".format(filename) for filename in files)
        else:
            lines.append("- 无")

        lines.append("")

    lines.extend([
        "## 未显式声明平台的模块",
        "",
        "- 共 {} 个。它们不等于“全平台支持”，只代表源码没有写清楚兼容边界。".format(
            len(report["unspecified"])
        ),
        "- {}".format(
            ", ".join("`{}`".format(name) for name in report["unspecified"])
        ),
        "",
        "## 可复现命令",
        "",
        "```bash",
        "cd /Users/pangxingzhong/.openclaw/workspace/Ghost",
        "python3 scripts/analyze_module_platforms.py",
        "python3 scripts/identify_generic_modules.py",
        "```",
        "",
    ])

    return "\n".join(lines)


def write_outputs(report):
    os.makedirs(DOCS_DIR, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    with open(MATRIX_PATH, "w", encoding="utf-8") as handle:
        handle.write(build_markdown(report))


def main():
    modules = load_modules()
    report = build_report(modules)
    write_outputs(report)

    print("=== Ghost 模块平台覆盖统计 ===")
    for platform in SUPPORTED_PLATFORMS:
        count = report["coverage"].get(platform)
        if count:
            print("  {}: {} modules".format(platform, count))

    print("\n总模块数: {}".format(report["module_total"]))
    print("未显式声明平台: {}".format(len(report["unspecified"])))
    print("报告已保存: {}".format(REPORT_PATH))
    print("矩阵已保存: {}".format(MATRIX_PATH))


if __name__ == "__main__":
    main()
