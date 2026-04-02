#!/usr/bin/env python3
"""
Fix hexadecimal literals in winstructures.py by removing 'L' suffix
"""

import re

# Path to the file
file_path = '/Users/pangxingzhong/.openclaw/workspace/Ghost/ghost/external/BeRoot/Windows/BeRoot/beroot/modules/objects/winstructures.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Replace all hex literals with 'L' suffix
content = re.sub(r'(0x[0-9A-Fa-f]+)L', r'\1', content)

# Write the fixed content back
with open(file_path, 'w') as f:
    f.write(content)

print(f"Fixed hexadecimal literals in {file_path}")