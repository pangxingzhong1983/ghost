#!/usr/bin/env python3
import os
import re

def fix_escape_sequences(directory):
    """修复Python文件中的转义序列警告"""
    # 遍历所有Python文件
    for root, dirs, files in os.walk(directory):
        # 跳过虚拟环境目录
        dirs[:] = [d for d in dirs if d not in ['.pyi-venv', 'ghostvenv', '__pycache__']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'处理文件: {file_path}')
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    # 处理每一行
                    fixed_lines = []
                    for line in lines:
                        # 修复正则表达式中的转义序列
                        if 're.compile' in line or 're.search' in line or 're.match' in line:
                            # 处理常见的正则表达式转义
                            line = line.replace('\\d', '\\\\d')
                            line = line.replace('\\D', '\\\\D')
                            line = line.replace('\\w', '\\\\w')
                            line = line.replace('\\W', '\\\\W')
                            line = line.replace('\\s', '\\\\s')
                            line = line.replace('\\S', '\\\\S')
                            line = line.replace('\\[', '\\\\[')
                            line = line.replace('\\]', '\\\\]')
                            line = line.replace('\\.', '\\\\.')
                            line = line.replace('\\+', '\\\\+')
                            line = line.replace('\\{', '\\\\{')
                            line = line.replace('\\}', '\\\\}')
                        
                        # 修复Windows路径中的反斜杠
                        if '\\\\' in line and ('os.path.join' in line or 'winreg.OpenKey' in line or 'open(' in line):
                            line = line.replace('\\', '\\\\')
                        
                        # 修复f-string中的反斜杠
                        if line.strip().startswith('f"') or line.strip().startswith("f'"):
                            line = line.replace('\\', '\\\\')
                        
                        fixed_lines.append(line)
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.writelines(fixed_lines)
                    
                    print(f'修复完成: {file_path}')
                except Exception as e:
                    print(f'处理文件 {file_path} 时出错: {e}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('用法: python fix_escape_sequences_simple.py <directory>')
        sys.exit(1)
    
    directory = sys.argv[1]
    fix_escape_sequences(directory)