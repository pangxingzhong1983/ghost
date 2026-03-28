#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ghost 模块平台覆盖分析器
扫描 ghost/modules 下所有 .py 文件，提取 @config(compatibilities=[...]) 信息
输出：
  - 覆盖率统计
  - 各平台模块清单
  - 缺失 darwin/linux/android 的模块列表
  - 可快速补全的“平台无关”模块建议
"""

import os
import re
import json
from collections import defaultdict

MODULES_DIR = os.path.join(os.path.dirname(__file__), '..', 'ghost', 'modules')
MODULES_DIR = os.path.abspath(MODULES_DIR)

def extract_config_info(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
    # 提取 @config(...compatibilities=[...]...)
    m = re.search(r'@config\([^)]*compatibilities=\[(.*?)\]', txt, re.DOTALL)
    platforms = []
    if m:
        try:
            platforms = eval('[' + m.group(1) + ']')
        except Exception as e:
            pass
    # 类名
    class_match = re.search(r'__class_name__="([^"]+)"', txt)
    class_name = class_match.group(1) if class_match else None
    # @config(cat=...) 分类
    cat_match = re.search(r'@config\([^)]*cat=["\']([^"\']+)["\']', txt, re.DOTALL)
    category = cat_match.group(1) if cat_match else None
    return {
        'file': os.path.basename(filepath),
        'class_name': class_name,
        'category': category,
        'platforms': platforms
    }

def main():
    all_files = []
    platform_index = defaultdict(list)
    for fn in os.listdir(MODULES_DIR):
        if fn.endswith('.py') and fn != '__init__.py':
            fp = os.path.join(MODULES_DIR, fn)
            info = extract_config_info(fp)
            all_files.append(info)
            for p in info['platforms']:
                platform_index[p].append(fn)

    # 输出统计
    print("=== Ghost 模块平台覆盖统计 ===")
    for p in sorted(platform_index.keys()):
        print(f"  {p}: {len(platform_index[p])} modules")
    print(f"\n总模块数: {len(all_files)}")
    darwin_set = set(platform_index.get('darwin', []))
    print(f"已支持 darwin: {len(darwin_set)}")
    missing = [f['file'] for f in all_files if f['file'] not in darwin_set]
    print(f"缺失 darwin: {len(missing)}")

    # 可快速补全：先找那些逻辑明显平台无关的模块
    print("\n=== 建议优先补全（可能无需改代码，仅加声明）===")
    quick_wins = []
    for f in all_files:
        if f['file'] in darwin_set:
            continue
        # 判断是否跨平台潜力：
        # - 不使用 windows-only 库（如 winreg, pywin32, ntpath 为主）
        # - 不包含进程注入/COM 等 Windows 特有操作
        # - 类名和描述看起来是通用功能
        plat = f['platforms']
        if 'windows' not in plat:
            continue  # 本身非 Windows 专属，但缺乏 darwin
        quick_wins.append(f['file'])
    print(", ".join(quick_wins[:30]))

    # 输出缺失清单（前50）
    print("\n=== 缺失 darwin 的模块（前50）===")
    for fn in missing[:50]:
        print(fn)

    # 写入 JSON 报告
    report = {
        'coverage': {p: len(platform_index[p]) for p in platform_index},
        'all_modules': all_files,
        'missing_darwin': missing,
        'quick_win_candidates': quick_wins
    }
    report_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'module_platform_report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n报告已保存: {report_path}")

if __name__ == '__main__':
    main()
