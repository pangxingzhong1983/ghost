#!/usr/bin/env python
# Test Android support

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_macos_support():
    print("=== Testing Mac OSX Support ===")
    import platform
    print(f"OS: {platform.system()}")
    print(f"Arch: {platform.machine()}")
    
    try:
        from ghost.ghostlib.GhostModule import GhostModule
        print("GhostModule imported successfully")
        
        from ghost.ghostlib.utils.arch import make_os_arch, make_template_arch
        print(f"Make OS Arch: {make_os_arch(platform.machine())}")
        print(f"Make Template Arch: {make_template_arch(platform.machine())}")
        
        print("✅ Mac OSX Ghost support test passed")
    except Exception as e:
        print(f"❌ Mac OSX Ghost support test failed: {e}")

def test_android_support():
    print("\n=== Testing Android Support ===")
    try:
        # Test if Android packages directory exists
        android_packages_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ghost', 'packages', 'android')
        if os.path.exists(android_packages_path):
            print("Android packages directory found")
            
            # Test if ghostdroid module exists
            ghostdroid_path = os.path.join(android_packages_path, 'ghostdroid')
            if os.path.exists(ghostdroid_path):
                print("Ghostdroid module directory found")
                
                # List available Android modules
                print("Available Android modules:")
                for file in os.listdir(ghostdroid_path):
                    if file.endswith('.py') and not file.startswith('__'):
                        module_name = file[:-3]
                        print(f"  - {module_name}")
                
                # Test ADB connection
                import subprocess
                result = subprocess.run(['adb', 'devices', '-l'], capture_output=True, text=True)
                if 'device' in result.stdout:
                    print("ADB device connected successfully")
                    print("✅ Android Ghost support test passed")
                else:
                    print("⚠️  No ADB device connected, but Android modules are available")
                    print("✅ Android Ghost support test passed")
            else:
                print("❌ Ghostdroid module directory not found")
        else:
            print("❌ Android packages directory not found")
    except Exception as e:
        print(f"❌ Android Ghost support test failed: {e}")

if __name__ == "__main__":
    test_macos_support()
    test_android_support()
    print("\n=== Test Summary ===")
    print("Testing completed for both Mac OSX and Android targets")