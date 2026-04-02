#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Comprehensive test script for antivirus evasion module

import os
import sys
import tempfile
import time
import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghost.ghostlib.GhostConfig import GhostConfig
from ghost.ghostlib.utils.antivirus_evasion import AntivirusEvasion
from ghost.ghostlib.utils.antivirus_evasion_update import AntivirusEvasionUpdater

class TestResult:
    def __init__(self, test_name, passed, message):
        self.test_name = test_name
        self.passed = passed
        self.message = message

class ComprehensiveTest:
    def __init__(self):
        self.config = GhostConfig()
        self.av_evasion = AntivirusEvasion(self.config)
        self.av_updater = AntivirusEvasionUpdater(self.config)
        self.results = []
    
    def run_test(self, test_name, test_func):
        """Run a test and record the result"""
        try:
            result = test_func()
            self.results.append(TestResult(test_name, True, result))
            print(f"✅ {test_name}: PASSED - {result}")
        except Exception as e:
            self.results.append(TestResult(test_name, False, str(e)))
            print(f"❌ {test_name}: FAILED - {str(e)}")
    
    def test_initialization(self):
        """Test module initialization"""
        assert self.av_evasion is not None
        assert self.av_updater is not None
        return "Module initialization successful"
    
    def test_update_check(self):
        """Test update check functionality"""
        result = self.av_evasion.check_for_updates()
        assert result is True
        return "Update check successful"
    
    def test_powershell_obfuscation(self):
        """Test PowerShell script obfuscation"""
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
        self.av_evasion.evasion_techniques['powershell']['current_technique'] = 'basic'
        print("Testing basic PowerShell obfuscation...")
        basic_obfuscated = self.av_evasion.obfuscate_powershell_script(ps_script)
        print(f"Basic obfuscated length: {len(basic_obfuscated)}")
        assert len(basic_obfuscated) > 0
        
        # Test medium obfuscation
        self.av_evasion.evasion_techniques['powershell']['current_technique'] = 'medium'
        print("Testing medium PowerShell obfuscation...")
        medium_obfuscated = self.av_evasion.obfuscate_powershell_script(ps_script)
        print(f"Medium obfuscated length: {len(medium_obfuscated)}")
        assert len(medium_obfuscated) > len(basic_obfuscated)
        
        # Test advanced obfuscation
        self.av_evasion.evasion_techniques['powershell']['current_technique'] = 'advanced'
        print("Testing advanced PowerShell obfuscation...")
        advanced_obfuscated = self.av_evasion.obfuscate_powershell_script(ps_script)
        print(f"Advanced obfuscated length: {len(advanced_obfuscated)}")
        assert len(advanced_obfuscated) > len(medium_obfuscated)
        
        return "PowerShell obfuscation test successful"
    
    def test_python_obfuscation(self):
        """Test Python script obfuscation"""
        python_script = '''
def test_function():
    # This is a test Python script
    print("Hello, world!")
    for i in range(10):
        print(f"Iteration {i}")
'''
        
        # Test basic obfuscation
        self.av_evasion.evasion_techniques['python']['current_technique'] = 'basic'
        basic_obfuscated = self.av_evasion.obfuscate_python_script(python_script)
        assert len(basic_obfuscated) >= len(python_script)
        
        # Test medium obfuscation
        self.av_evasion.evasion_techniques['python']['current_technique'] = 'medium'
        medium_obfuscated = self.av_evasion.obfuscate_python_script(python_script)
        assert len(medium_obfuscated) > len(basic_obfuscated)
        
        # Test advanced obfuscation
        self.av_evasion.evasion_techniques['python']['current_technique'] = 'advanced'
        advanced_obfuscated = self.av_evasion.obfuscate_python_script(python_script)
        assert len(advanced_obfuscated) > len(medium_obfuscated)
        
        return "Python obfuscation test successful"
    
    def test_binary_packing(self):
        """Test binary packing"""
        # Create a test binary file
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp:
            # Write a simple PE header
            tmp.write(b'MZ' + b'\x00' * 58 + b'PE' + b'\x00' * 2)
            test_binary_path = tmp.name
        
        try:
            # Test UPX packing
            self.av_evasion.evasion_techniques['binary']['current_packer'] = 'upx'
            upx_result = self.av_evasion.pack_binary(test_binary_path)
            
            # Test MPRESS packing
            self.av_evasion.evasion_techniques['binary']['current_packer'] = 'mpress'
            mpress_result = self.av_evasion.pack_binary(test_binary_path)
            
            # Test custom packing
            self.av_evasion.evasion_techniques['binary']['current_packer'] = 'custom'
            custom_result = self.av_evasion.pack_binary(test_binary_path)
            
            # Custom packing should always succeed
            assert custom_result is True
            
            return f"Binary packing test successful (UPX: {upx_result}, MPRESS: {mpress_result}, Custom: {custom_result})"
        finally:
            # Clean up
            if os.path.exists(test_binary_path):
                os.unlink(test_binary_path)
    
    def test_evasion_test(self):
        """Test evasion test functionality"""
        # Create a test payload file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as tmp:
            tmp.write(b'Write-Host "Test"')
            test_payload_path = tmp.name
        
        try:
            # Test evasion
            test_result = self.av_evasion.test_evasion(test_payload_path)
            assert 'detection_result' in test_result
            assert 'detected' in test_result['detection_result']
            
            return "Evasion test functionality successful"
        finally:
            # Clean up
            if os.path.exists(test_payload_path):
                os.unlink(test_payload_path)
    
    def test_report_generation(self):
        """Test report generation"""
        report = self.av_evasion.generate_evasion_report()
        assert 'timestamp' in report
        assert 'signature_database' in report
        assert 'evasion_techniques' in report
        assert 'test_results' in report
        
        return "Report generation successful"
    
    def test_updater(self):
        """Test updater functionality"""
        # Start the updater
        self.av_updater.start()
        time.sleep(2)  # Wait for updater to start
        
        # Check status
        status = self.av_updater.get_status()
        assert status['running'] is True
        
        # Stop the updater
        self.av_updater.stop()
        time.sleep(2)  # Wait for updater to stop
        
        # Check status again
        status = self.av_updater.get_status()
        assert status['running'] is False
        
        return "Updater functionality successful"
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n=== Comprehensive Antivirus Evasion Test ===")
        print(f"Date: {datetime.datetime.now().isoformat()}")
        print("=" * 60)
        
        tests = [
            ("Module Initialization", self.test_initialization),
            ("Update Check", self.test_update_check),
            ("PowerShell Obfuscation", self.test_powershell_obfuscation),
            ("Python Obfuscation", self.test_python_obfuscation),
            ("Binary Packing", self.test_binary_packing),
            ("Evasion Test", self.test_evasion_test),
            ("Report Generation", self.test_report_generation),
            ("Updater Functionality", self.test_updater)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        print("=" * 60)
        print("\n=== Test Summary ===")
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        print(f"Passed: {passed}/{total}")
        
        if passed == total:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed:")
            for result in self.results:
                if not result.passed:
                    print(f"  - {result.test_name}: {result.message}")
        
        return passed == total

if __name__ == "__main__":
    test = ComprehensiveTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)