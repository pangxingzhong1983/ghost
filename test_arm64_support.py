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
    print("=== System Information ===")
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