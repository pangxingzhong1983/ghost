#!/usr/bin/env python3
import os
import re
import fileinput

def fix_syntax_errors(directory):
    """自动修复常见的Python语法错误"""
    # 要修复的模式
    patterns = {
        # print语句缺少括号
        r'^\s*print\s+([^\(].*)$': r'print(\1)',
        # isinstance语法错误
        r'isinstance\(([^,]+)\s+([^:]+):\)': r'isinstance(\1, \2):',
        # except Exception e语法
        r'except\s+([A-Za-z0-9_]+)\s+([a-z0-9_]+):': r'except \1 as \2:',
        # async关键字错误（将async变量名改为async_handle）
        r'\basync\s*=\s*': r'async_handle = ',
        r'\bself\.async\b': r'self.async_handle',
        r'\basync\b\s*\.': r'async_handle.',
        r'\bglobal\s+async\b': r'global async_handle',
        # rpyc.async语法错误
        r'rpyc\.async\(': r'rpyc.async_(',
    }
    
    # 遍历所有Python文件
    for root, dirs, files in os.walk(directory):
        # 跳过虚拟环境目录
        dirs[:] = [d for d in dirs if d not in ['.pyi-venv', 'ghostvenv', '__pycache__']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'处理文件: {file_path}')
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 应用修复
                for pattern, replacement in patterns.items():
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
                
                print(f'修复完成: {file_path}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('用法: python fix_syntax_errors.py <directory>')
        sys.exit(1)
    
    directory = sys.argv[1]
    fix_syntax_errors(directory)