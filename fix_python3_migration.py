#!/usr/bin/env python3
"""
Script to fix Python 2 to Python 3 migration issues in Ghost
"""

import os
import re

# Directories to process
TARGET_DIRS = ["ghost"]

# Patterns to replace
REPLACEMENTS = [
    # Replace long with int
    (r'\blong\b', 'int'),
    # Replace xrange with range
    (r'\bxrange\b', 'range'),
    # Replace iteritems() with items()
    (r'\.iteritems\(\)', '.items()'),
    # Replace iterkeys() with keys()
    (r'\.iterkeys\(\)', '.keys()'),
    # Replace itervalues() with values()
    (r'\.itervalues\(\)', '.values()'),
    # Replace print statement with print function
    (r'^\s*print\s+(.*)$', r'print(\1)'),
    # Replace % formatting with f-strings where possible
    (r'"(.*)"\s*%\s*\((.*)\)', lambda m: f'f"{m.group(1).replace("%s", "{}")}" % ({m.group(2)})'),
]

def fix_file(filepath):
    """Fix Python 2 to Python 3 issues in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply replacements
        original_content = content
        for pattern, replacement in REPLACEMENTS:
            if callable(replacement):
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            else:
                content = re.sub(pattern, replacement, content)
        
        # Fix type comparisons
        content = re.sub(r'type\((.*)\)\s*==\s*(.*)', r'isinstance(\1, \2)', content)
        content = re.sub(r'type\((.*)\)\s*!=\s*(.*)', r'not isinstance(\1, \2)', content)
        
        # Write back if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory):
    """Process all Python files in a directory"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                fix_file(filepath)

if __name__ == "__main__":
    for directory in TARGET_DIRS:
        if os.path.exists(directory):
            print(f"Processing directory: {directory}")
            process_directory(directory)
        else:
            print(f"Directory not found: {directory}")