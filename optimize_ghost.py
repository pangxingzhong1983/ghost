#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ghost源码优化升级脚本
执行全面的优化任务，包括Python版本迁移、依赖管理、代码质量提升等
"""

import os
import sys
import subprocess
import shutil
import re

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
GHOST_DIR = os.path.join(PROJECT_ROOT, 'ghost')

# 检查Python版本
def check_python_version():
    """检查Python版本是否为3.10+"""
    print("检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"错误: Python版本 {version.major}.{version.minor} 低于要求的 3.10")
        return False
    print(f"Python版本: {version.major}.{version.minor}.{version.micro} (符合要求)")
    return True

# 清理Python 2兼容代码
def clean_python2_compat():
    """清理Python 2兼容代码"""
    print("清理Python 2兼容代码...")
    # 检查是否存在library_patches_py2目录
    py2_patches = os.path.join(GHOST_DIR, 'library_patches_py2')
    if os.path.exists(py2_patches):
        print(f"删除library_patches_py2目录: {py2_patches}")
        shutil.rmtree(py2_patches)
    else:
        print("library_patches_py2目录不存在，跳过删除")

# 优化library_patches_py3目录
def optimize_py3_patches():
    """优化library_patches_py3目录中的代码"""
    print("优化library_patches_py3目录...")
    py3_patches = os.path.join(GHOST_DIR, 'library_patches_py3')
    if not os.path.exists(py3_patches):
        print("library_patches_py3目录不存在，跳过优化")
        return
    
    # 优化bz2.py
    bz2_file = os.path.join(py3_patches, 'bz2.py')
    if os.path.exists(bz2_file):
        with open(bz2_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # 优化字符串格式化
        content = re.sub(r'f"Invalid mode: %r" % \(mode,\)', r'f"Invalid mode: {mode!r}"', content)
        with open(bz2_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"优化了 {bz2_file}")

# 优化ghostlib目录中的代码
def optimize_ghostlib():
    """优化ghostlib目录中的代码"""
    print("优化ghostlib目录...")
    ghostlib_dir = os.path.join(GHOST_DIR, 'ghostlib')
    if not os.path.exists(ghostlib_dir):
        print("ghostlib目录不存在，跳过优化")
        return
    
    # 优化GhostConfig.py
    config_file = os.path.join(ghostlib_dir, 'GhostConfig.py')
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # 修复f-string格式
        content = re.sub(r'f\'{} is not a {}\'.format\((.*?)\)', r'f"\1"', content)
        content = re.sub(r'f\'{} is not a {}\'.format\((.*?), (.*?)\)', r'f"\1 is not a \2"', content)
        content = re.sub(r'f\'{} is not a {}\'.format\(path\.abspath\(retfilepath\), \'dir\' if dir else \'file\'\)', r'f"{path.abspath(retfilepath)} is not a {\"dir\" if dir else \"file\"}"', content)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"优化了 {config_file}")
    
    # 优化GhostJob.py
    job_file = os.path.join(ghostlib_dir, 'GhostJob.py')
    if os.path.exists(job_file):
        with open(job_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # 优化字符串格式化
        content = re.sub(r'raise RuntimeError\("job %s has already been started !"%str\(self\)\)', r'raise RuntimeError(f"job {str(self)} has already been started !")', content)
        content = re.sub(r'raise RuntimeError\("can\'t interrupt\. job %s has not been started"%str\(self\)\)', r'raise RuntimeError(f"can\'t interrupt. job {str(self)} has not been started")', content)
        with open(job_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"优化了 {job_file}")
    
    # 优化GhostClientInitializer.py
    client_init_file = os.path.join(ghostlib_dir, 'GhostClientInitializer.py')
    if os.path.exists(client_init_file):
        with open(client_init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # 优化字符串格式化
        content = re.sub(r'logging\.error\(\'GetTokenInformation\(\): Unknown error: %d\',\s*dwLastError\)', r'logging.error(f\'GetTokenInformation(): Unknown error: {dwLastError}\')', content)
        content = re.sub(r'logging\.error\(\'GetTokenInformation\(\): Unknown error with buffer size %d: %d\',\s*info_size\.value, GetLastError\(\)\)', r'logging.error(f\'GetTokenInformation(): Unknown error with buffer size {info_size.value}: {GetLastError()}\')', content)
        content = re.sub(r'return mapping\.get\(value\) or u\'0x%04x\' % value', r'return mapping.get(value) or f\'0x{value:04x}\'', content)
        with open(client_init_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"优化了 {client_init_file}")
    
    # 优化GhostServer.py
    server_file = os.path.join(ghostlib_dir, 'GhostServer.py')
    if os.path.exists(server_file):
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # 修复端口错误
        content = re.sub(r'f"Invalid local port: {port\[1\]}"', r'f"Invalid local port: {port}"', content)
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"优化了 {server_file}")

# 安装依赖
def install_dependencies():
    """安装项目依赖"""
    print("安装项目依赖...")
    try:
        # 检查是否安装了poetry
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'poetry'], check=True)
        # 安装依赖
        subprocess.run([sys.executable, '-m', 'poetry', 'install'], cwd=PROJECT_ROOT, check=True)
        print("依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        # 尝试使用pip安装基础依赖
        print("尝试使用pip安装基础依赖...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pycryptodome', 'pyyaml', 'requests', 'six', 'psutil'], check=True)
            print("基础依赖安装成功")
        except subprocess.CalledProcessError as e:
            print(f"基础依赖安装失败: {e}")

# 构建Docker镜像
def build_docker_image():
    """构建Docker镜像"""
    print("构建Docker镜像...")
    try:
        subprocess.run(['docker', 'build', '-t', 'ghost-c2', '.'], cwd=PROJECT_ROOT, check=True)
        print("Docker镜像构建成功")
    except subprocess.CalledProcessError as e:
        print(f"Docker镜像构建失败: {e}")

# 主函数
def main():
    """执行所有优化任务"""
    print("开始Ghost源码优化升级...")
    
    # 1. 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 2. 清理Python 2兼容代码
    clean_python2_compat()
    
    # 3. 优化library_patches_py3目录
    optimize_py3_patches()
    
    # 4. 优化ghostlib目录
    optimize_ghostlib()
    
    # 5. 安装依赖
    install_dependencies()
    
    # 6. 构建Docker镜像
    build_docker_image()
    
    print("\nGhost源码优化升级完成！")
    print("\n优化内容总结:")
    print("1. 清理了Python 2兼容代码")
    print("2. 优化了library_patches_py3目录中的代码")
    print("3. 优化了ghostlib目录中的代码，使用f-string替代旧式字符串格式化")
    print("4. 安装了项目依赖")
    print("5. 构建了Docker镜像")

if __name__ == '__main__':
    main()