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
                        content = f.read()
                    
                    # 修复正则表达式中的转义序列
                    # 处理 \d, \D, \w, \W, \s, \S 等正则表达式转义
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\d([^"\']*)(["\'])', r'\1(\2\3\\\\d\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\D([^"\']*)(["\'])', r'\1(\2\3\\\\D\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\w([^"\']*)(["\'])', r'\1(\2\3\\\\w\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\W([^"\']*)(["\'])', r'\1(\2\3\\\\W\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\s([^"\']*)(["\'])', r'\1(\2\3\\\\s\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\S([^"\']*)(["\'])', r'\1(\2\3\\\\S\4', content)
                    
                    # 处理方括号转义
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\[([^"\']*)(["\'])', r'\1(\2\3\\\\[\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\]([^"\']*)(["\'])', r'\1(\2\3\\\\]\4', content)
                    
                    # 处理点号转义
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\.([^"\']*)(["\'])', r'\1(\2\3\\\\.\4', content)
                    
                    # 处理加号转义
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\+([^"\']*)(["\'])', r'\1(\2\3\\\\+\4', content)
                    
                    # 处理花括号转义
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\{([^"\']*)(["\'])', r'\1(\2\3\\\\{\4', content)
                    content = re.sub(r'(re\.compile|re\.search|re\.match)\((["\'])([^"\']*)\\}([^"\']*)(["\'])', r'\1(\2\3\\\\}\4', content)
                    
                    # 处理Windows路径中的反斜杠
                    content = re.sub(r'(open|os\.path\.join|winreg\.OpenKey)\([^)]*\\([^\\n\r\)])', r'\1(\2\\\\\3', content)
                    
                    # 处理f-string中的反斜杠
                    content = re.sub(r'f(["\'])([^"\']*)\\([^"\']*)(["\'])', r'f\1\2\\\\\3\4', content)
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(content)
                    
                    print(f'修复完成: {file_path}')
                except Exception as e:
                    print(f'处理文件 {file_path} 时出错: {e}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('用法: python fix_escape_sequences.py <directory>')
        sys.exit(1)
    
    directory = sys.argv[1]
    fix_escape_sequences(directory)