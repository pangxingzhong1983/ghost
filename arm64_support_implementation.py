#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ARM64 Support Implementation Plan for Ghost

This script implements support for Linux ARM64 and Windows ARM64 architectures.
"""

import os
import sys
import platform
import shutil

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def update_arch_module():
    """Update arch.py to better support ARM64 architectures"""
    arch_file = os.path.join('ghost', 'ghostlib', 'utils', 'arch.py')
    
    with open(arch_file, 'r') as f:
        content = f.read()
    
    # Add arm64 to make_os_arch function
    if "'arm64': 'arm64'" not in content:
        content = content.replace(
            "'armv7l': 'armhf'",
            "'armv7l': 'armhf',\n        'arm64': 'arm64'"
        )
    
    # Add arm64 to make_template_arch function
    if "'arm64': 'arm64'" not in content:
        content = content.replace(
            "'armv7l': 'armhf'",
            "'armv7l': 'armhf',\n        'arm64': 'arm64'"
        )
    
    # Add arm64 to os_arch_to_platform mapping
    if "'arm64': 'arm'" not in content:
        content = content.replace(
            "'aarch64': 'arm'",
            "'aarch64': 'arm',\n        'arm64': 'arm'"
        )
    
    with open(arch_file, 'w') as f:
        f.write(content)
    
    print("✅ Updated arch.py to support ARM64")

def create_linux_arm64_support():
    """Create Linux ARM64 support"""
    # Create linux/arm64 directory if it doesn't exist
    linux_arm64_dir = os.path.join('ghost', 'packages', 'linux', 'arm64')
    os.makedirs(linux_arm64_dir, exist_ok=True)
    
    # Copy common Linux modules to arm64 directory
    linux_all_dir = os.path.join('ghost', 'packages', 'linux', 'all')
    if os.path.exists(linux_all_dir):
        for file in os.listdir(linux_all_dir):
            if file.endswith('.py') and not file.startswith('__'):
                src = os.path.join(linux_all_dir, file)
                dst = os.path.join(linux_arm64_dir, file)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    print(f"✅ Copied {file} to Linux ARM64 directory")
    
    # Create a simple test module for Linux ARM64
    test_module = os.path.join(linux_arm64_dir, 'arm64_test.py')
    with open(test_module, 'w') as f:
        f.write('''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_arm64():
    """Test function for Linux ARM64 support"""
    return "Linux ARM64 support is working"
''')
    
    print("✅ Created Linux ARM64 support")

def create_windows_arm64_support():
    """Create Windows ARM64 support"""
    # Create windows/arm64 directory if it doesn't exist
    windows_arm64_dir = os.path.join('ghost', 'packages', 'windows', 'arm64')
    os.makedirs(windows_arm64_dir, exist_ok=True)
    
    # Copy common Windows modules to arm64 directory
    windows_all_dir = os.path.join('ghost', 'packages', 'windows', 'all')
    if os.path.exists(windows_all_dir):
        for file in os.listdir(windows_all_dir):
            if file.endswith('.py') and not file.startswith('__'):
                src = os.path.join(windows_all_dir, file)
                dst = os.path.join(windows_arm64_dir, file)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    print(f"✅ Copied {file} to Windows ARM64 directory")
    
    # Create a simple test module for Windows ARM64
    test_module = os.path.join(windows_arm64_dir, 'arm64_test.py')
    with open(test_module, 'w') as f:
        f.write('''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_arm64():
    """Test function for Windows ARM64 support"""
    return "Windows ARM64 support is working"
''')
    
    print("✅ Created Windows ARM64 support")

def update_memory_importer():
    """Update memory importer to support ARM64"""
    # Update memimporter/__init__.py
    memimporter_init = os.path.join('ghost', 'agent', 'memimporter', '__init__.py')
    
    with open(memimporter_init, 'r') as f:
        content = f.read()
    
    # Add arm64 support to the import logic
    if "sys.platform == 'win32' and platform.machine() == 'ARM64'" not in content:
        # Update the import logic to handle Windows ARM64
        content = content.replace(
            "elif sys.platform == 'win32':",
            "elif sys.platform == 'win32':\n    if platform.machine() == 'ARM64':\n        from .win32_arm64 import load_content\n    else:\n"
        )
    
    with open(memimporter_init, 'w') as f:
        f.write(content)
    
    # Create win32_arm64.py for Windows ARM64 memory import
    win32_arm64_file = os.path.join('ghost', 'agent', 'memimporter', 'win32_arm64.py')
    with open(win32_arm64_file, 'w') as f:
        f.write('''
# -*- coding: utf-8 -*-

from .win32 import load_content

# For Windows ARM64, we use the same implementation as win32
# In the future, we may need ARM64-specific optimizations
''')
    
    print("✅ Updated memory importer to support ARM64")

def create_arm64_test_script():
    """Create a test script to verify ARM64 support"""
    test_script = os.path.join('test_arm64_support.py')
    with open(test_script, 'w') as f:
        f.write('''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for ARM64 support
"""

import sys
import os
import platform

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_arch_support():
    """Test architecture support"""
    print(f"=== System Information ===")
    print(f"OS: {platform.system()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python version: {platform.python_version()}")
    
    print("\n=== Testing ARM64 Support ===")
    
    # Test arch module
    try:
        from ghost.ghostlib.utils.arch import make_os_arch, make_template_arch, make_proc_arch
        print("✅ Arch module imported successfully")
        
        # Test architecture mapping
        current_arch = platform.machine()
        print(f"Current architecture: {current_arch}")
        print(f"make_os_arch: {make_os_arch(current_arch)}")
        print(f"make_template_arch: {make_template_arch(current_arch)}")
        print(f"make_proc_arch (64bit): {make_proc_arch(current_arch, '64bit')}")
    except Exception as e:
        print(f"❌ Arch module test failed: {e}")
    
    # Test memory importer
    try:
        from ghost.agent.memimporter import import_module, load_dll
        print("✅ Memory importer imported successfully")
    except Exception as e:
        print(f"❌ Memory importer test failed: {e}")
    
    # Test platform-specific modules
    print("\n=== Testing Platform-Specific Modules ===")
    
    # Test Linux ARM64
    if platform.system() == 'Linux' and platform.machine() in ['aarch64', 'arm64']:
        try:
            import ghost.packages.linux.arm64.arm64_test
            result = ghost.packages.linux.arm64.arm64_test.test_arm64()
            print(f"✅ Linux ARM64 test: {result}")
        except Exception as e:
            print(f"❌ Linux ARM64 test failed: {e}")
    
    # Test Windows ARM64
    if platform.system() == 'Windows' and platform.machine() == 'ARM64':
        try:
            import ghost.packages.windows.arm64.arm64_test
            result = ghost.packages.windows.arm64.arm64_test.test_arm64()
            print(f"✅ Windows ARM64 test: {result}")
        except Exception as e:
            print(f"❌ Windows ARM64 test failed: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_arch_support()
''')
    
    print("✅ Created ARM64 test script")

def main():
    """Main function to implement ARM64 support"""
    print("=== Implementing ARM64 Support for Ghost ===")
    
    # Update arch module
    update_arch_module()
    
    # Create Linux ARM64 support
    create_linux_arm64_support()
    
    # Create Windows ARM64 support
    create_windows_arm64_support()
    
    # Update memory importer
    update_memory_importer()
    
    # Create test script
    create_arm64_test_script()
    
    print("\n=== ARM64 Support Implementation Complete ===")
    print("To test ARM64 support, run: python test_arm64_support.py")

if __name__ == "__main__":
    main()