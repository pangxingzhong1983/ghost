#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Test script for antivirus evasion module

import os
import sys
import tempfile

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghost.ghostlib.GhostConfig import GhostConfig
from ghost.ghostlib.utils.antivirus_evasion import AntivirusEvasion


# Initialize configuration
config = GhostConfig()

# Initialize antivirus evasion module
av_evasion = AntivirusEvasion(config)

# Test 1: Check for updates
print("=== Test 1: Checking for updates ===")
av_evasion.check_for_updates()
print(f"Evasion status: {av_evasion.get_evasion_status()}")

# Test 2: Test PowerShell script obfuscation
print("\n=== Test 2: PowerShell script obfuscation ===")
ps_script = '''
function Invoke-ReflectivePEInjection {
    param(
        [Parameter(Mandatory=$true)]
        [Byte[]]$PEBytes,
        [Parameter(Mandatory=$false)]
        [Switch]$ForceASLR
    )
    # This is a test PowerShell script
    Write-Host "Injecting PE..."
}
'''

# Test basic obfuscation
av_evasion.evasion_techniques['powershell']['current_technique'] = 'basic'
basic_obfuscated = av_evasion.obfuscate_powershell_script(ps_script)
print(f"Basic obfuscation result length: {len(basic_obfuscated)}")
print(f"Basic obfuscation sample: {basic_obfuscated[:200]}...")

# Test medium obfuscation
av_evasion.evasion_techniques['powershell']['current_technique'] = 'medium'
medium_obfuscated = av_evasion.obfuscate_powershell_script(ps_script)
print(f"\nMedium obfuscation result length: {len(medium_obfuscated)}")
print(f"Medium obfuscation sample: {medium_obfuscated[:200]}...")

# Test advanced obfuscation
av_evasion.evasion_techniques['powershell']['current_technique'] = 'advanced'
advanced_obfuscated = av_evasion.obfuscate_powershell_script(ps_script)
print(f"\nAdvanced obfuscation result length: {len(advanced_obfuscated)}")
print(f"Advanced obfuscation sample: {advanced_obfuscated[:200]}...")

# Test 3: Test Python script obfuscation
print("\n=== Test 3: Python script obfuscation ===")
python_script = '''
def test_function():
    # This is a test Python script
    print("Hello, world!")
    for i in range(10):
        print(f"Iteration {i}")
'''

# Test basic obfuscation
av_evasion.evasion_techniques['python']['current_technique'] = 'basic'
basic_obfuscated_py = av_evasion.obfuscate_python_script(python_script)
print(f"Basic obfuscation result length: {len(basic_obfuscated_py)}")
print(f"Basic obfuscation sample: {basic_obfuscated_py[:200]}...")

# Test medium obfuscation
av_evasion.evasion_techniques['python']['current_technique'] = 'medium'
medium_obfuscated_py = av_evasion.obfuscate_python_script(python_script)
print(f"\nMedium obfuscation result length: {len(medium_obfuscated_py)}")
print(f"Medium obfuscation sample: {medium_obfuscated_py[:200]}...")

# Test advanced obfuscation
av_evasion.evasion_techniques['python']['current_technique'] = 'advanced'
advanced_obfuscated_py = av_evasion.obfuscate_python_script(python_script)
print(f"\nAdvanced obfuscation result length: {len(advanced_obfuscated_py)}")
print(f"Advanced obfuscation sample: {advanced_obfuscated_py[:200]}...")

# Test 4: Test binary packing
print("\n=== Test 4: Binary packing ===")

# Create a test binary file
with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp:
    # Write a simple PE header
    tmp.write(b'MZ' + b'\x00' * 58 + b'PE' + b'\x00' * 2)
    test_binary_path = tmp.name

try:
    # Test UPX packing
    av_evasion.evasion_techniques['binary']['current_packer'] = 'upx'
    upx_result = av_evasion.pack_binary(test_binary_path)
    print(f"UPX packing result: {upx_result}")
    
    # Test MPRESS packing
    av_evasion.evasion_techniques['binary']['current_packer'] = 'mpress'
    mpress_result = av_evasion.pack_binary(test_binary_path)
    print(f"MPRESS packing result: {mpress_result}")
    
    # Test custom packing
    av_evasion.evasion_techniques['binary']['current_packer'] = 'custom'
    custom_result = av_evasion.pack_binary(test_binary_path)
    print(f"Custom packing result: {custom_result}")
finally:
    # Clean up
    if os.path.exists(test_binary_path):
        os.unlink(test_binary_path)

# Test 5: Test evasion test
print("\n=== Test 5: Evasion test ===")

# Create a test payload file
with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as tmp:
    tmp.write(ps_script.encode('utf-8'))
    test_payload_path = tmp.name

try:
    # Test evasion
    test_result = av_evasion.test_evasion(test_payload_path)
    print(f"Evasion test result: {test_result}")
except Exception as e:
    print(f"Error during evasion test: {e}")
finally:
    # Clean up
    if os.path.exists(test_payload_path):
        os.unlink(test_payload_path)

# Test 6: Generate evasion report
print("\n=== Test 6: Generate evasion report ===")
try:
    report = av_evasion.generate_evasion_report()
    print(f"Evasion report generated successfully")
    print(f"Report timestamp: {report['timestamp']}")
except Exception as e:
    print(f"Error generating evasion report: {e}")

print("\n=== All tests completed ===")