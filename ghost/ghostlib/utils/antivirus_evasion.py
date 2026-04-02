#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Ghost Project

# Ghost is under the BSD 3-Clause license. see the LICENSE file at the
# root of the project for the detailed licence terms

import os
import sys
import time
import random
import string
import subprocess
import datetime
import json
import hashlib
import shutil
import tempfile

from ghost.ghostlib.GhostLogger import getLogger
from ghost.ghostlib.GhostOutput import Success, Warn, Error, Info
from ghost.ghostlib.utils.downloader import download
from ghost.ghostlib.payloads.py_oneliner import pack_py_payload
from ghost.ghostlib.payloads.dotnet import DotNetPayload
from ghost.network.lib.convcompat import as_native_string

logger = getLogger('antivirus_evasion')

class AntivirusEvasion:
    def __init__(self, config):
        self.config = config
        self.evasion_techniques = {
            'powershell': {
                'obfuscation_levels': ['basic', 'medium', 'advanced'],
                'current_technique': 'basic',
                'last_updated': None
            },
            'python': {
                'obfuscation_levels': ['basic', 'medium', 'advanced'],
                'current_technique': 'basic',
                'last_updated': None
            },
            'binary': {
                'packers': ['upx', 'mpress', 'custom'],
                'current_packer': 'upx',
                'last_updated': None
            }
        }
        self.signature_database = {
            'av_vendors': [],
            'signatures': [],
            'last_updated': None
        }
        self.test_results = []
        self.update_interval = 24  # hours
        self.last_update_check = None
    
    def check_for_updates(self):
        """Check for updates to antivirus signatures and evasion techniques"""
        current_time = datetime.datetime.now()
        
        if self.last_update_check is None or \
           (current_time - self.last_update_check).total_seconds() / 3600 >= self.update_interval:
            logger.info('Checking for antivirus signature updates...')
            self.last_update_check = current_time
            
            # In a real implementation, this would check online sources for signature updates
            # For now, we'll simulate an update check
            self.update_signature_database()
            self.update_evasion_techniques()
            return True
        return False
    
    def update_signature_database(self):
        """Update the signature database with the latest antivirus signatures"""
        # Simulate updating signature database
        logger.info('Updating signature database...')
        self.signature_database['av_vendors'] = ['Windows Defender', 'Avast', 'Kaspersky', 'McAfee', 'Symantec']
        self.signature_database['signatures'] = [
            'Invoke-ReflectivePEInjection',
            'Mimikatz',
            'Ghost payload',
            'PowerShell obfuscation',
            'Python packed payload'
        ]
        self.signature_database['last_updated'] = datetime.datetime.now().isoformat()
        logger.info('Signature database updated successfully')
    
    def update_evasion_techniques(self):
        """Update evasion techniques based on the latest signature database"""
        logger.info('Updating evasion techniques...')
        
        # Update PowerShell obfuscation technique
        if 'Invoke-ReflectivePEInjection' in self.signature_database['signatures']:
            self.evasion_techniques['powershell']['current_technique'] = 'advanced'
        elif 'PowerShell obfuscation' in self.signature_database['signatures']:
            self.evasion_techniques['powershell']['current_technique'] = 'medium'
        else:
            self.evasion_techniques['powershell']['current_technique'] = 'basic'
        
        # Update Python obfuscation technique
        if 'Python packed payload' in self.signature_database['signatures']:
            self.evasion_techniques['python']['current_technique'] = 'advanced'
        else:
            self.evasion_techniques['python']['current_technique'] = 'basic'
        
        # Update binary packing technique
        self.evasion_techniques['binary']['current_packer'] = random.choice(self.evasion_techniques['binary']['packers'])
        
        for tech in self.evasion_techniques:
            self.evasion_techniques[tech]['last_updated'] = datetime.datetime.now().isoformat()
        
        logger.info('Evasion techniques updated successfully')
    
    def obfuscate_powershell_script(self, script):
        """Obfuscate PowerShell script based on current evasion technique"""
        technique = self.evasion_techniques['powershell']['current_technique']
        logger.info(f'Obfuscating PowerShell script with {technique} technique')
        
        # Basic obfuscation
        if technique == 'basic':
            from ghost.modules.lib.windows.powershell import obfuscatePowershellScript
            return obfuscatePowershellScript(script)
        
        # Medium obfuscation
        elif technique == 'medium':
            from ghost.modules.lib.windows.powershell import obfuscatePowershellScript
            obfuscated = obfuscatePowershellScript(script)
            # Add variable name obfuscation
            obfuscated = self._obfuscate_variable_names(obfuscated)
            return obfuscated
        
        # Advanced obfuscation
        elif technique == 'advanced':
            from ghost.modules.lib.windows.powershell import obfuscatePowershellScript
            obfuscated = obfuscatePowershellScript(script)
            # Add variable name obfuscation
            obfuscated = self._obfuscate_variable_names(obfuscated)
            # Add string encoding
            obfuscated = self._encode_strings(obfuscated)
            # Add control flow obfuscation
            obfuscated = self._obfuscate_control_flow(obfuscated)
            return obfuscated
    
    def _obfuscate_variable_names(self, script):
        """Obfuscate variable names in PowerShell script"""
        import re
        # Find all variable names
        variables = re.findall(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', script)
        # Create mapping of original variable names to obfuscated names
        var_map = {}
        for var in variables:
            if var not in var_map:
                obfuscated = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                var_map[var] = obfuscated
        # Replace variable names in script
        for var, obfuscated in var_map.items():
            script = re.sub(rf'\${var}\b', f'${obfuscated}', script)
        return script
    
    def _encode_strings(self, script):
        """Encode strings in PowerShell script"""
        import re
        # Find all strings
        strings = re.findall(r'"([^"]*)"', script)
        # Replace strings with encoded versions
        for string in strings:
            if len(string) > 3:
                encoded = ''.join([f'[char]{ord(c)}' for c in string])
                script = script.replace(f'"{string}"', f'({encoded}) -join ""')
        return script
    
    def _obfuscate_control_flow(self, script):
        """Obfuscate control flow in PowerShell script"""
        # Add random dead code
        dead_code = ''.join([f'if ($false) {{ Write-Host "{''.join(random.choices(string.ascii_letters, k=20))}" }}; ' for _ in range(5)])
        script = dead_code + script
        # Add random comments
        lines = script.split('\n')
        for i in range(len(lines)):
            if lines[i].strip() and not lines[i].strip().startswith('#'):
                comment = ''.join(random.choices(string.ascii_letters, k=10))
                lines[i] = f'{lines[i]} # {comment}'
        script = '\n'.join(lines)
        return script
    
    def obfuscate_python_script(self, script):
        """Obfuscate Python script based on current evasion technique"""
        technique = self.evasion_techniques['python']['current_technique']
        logger.info(f'Obfuscating Python script with {technique} technique')
        
        # Basic obfuscation
        if technique == 'basic':
            return script
        
        # Medium obfuscation
        elif technique == 'medium':
            # Add variable name obfuscation
            return self._obfuscate_python_variables(script)
        
        # Advanced obfuscation
        elif technique == 'advanced':
            # Add variable name obfuscation
            obfuscated = self._obfuscate_python_variables(script)
            # Add string encoding
            obfuscated = self._encode_python_strings(obfuscated)
            # Add control flow obfuscation
            obfuscated = self._obfuscate_python_control_flow(obfuscated)
            return obfuscated
    
    def _obfuscate_python_variables(self, script):
        """Obfuscate variable names in Python script"""
        import re
        # Find all variable names
        variables = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', script)
        # Exclude built-in functions and keywords
        keywords = ['def', 'class', 'import', 'from', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'return', 'yield', 'pass', 'break', 'continue', 'global', 'nonlocal', 'assert', 'raise', 'del', 'lambda', 'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None']
        variables = [var for var in variables if var not in keywords]
        # Create mapping of original variable names to obfuscated names
        var_map = {}
        for var in variables:
            if var not in var_map:
                obfuscated = ''.join(random.choices(string.ascii_letters, k=10))
                var_map[var] = obfuscated
        # Replace variable names in script
        for var, obfuscated in var_map.items():
            script = re.sub(rf'\b{var}\b', obfuscated, script)
        return script
    
    def _encode_python_strings(self, script):
        """Encode strings in Python script"""
        import re
        # Find all strings
        strings = re.findall(r'"([^"]*)"', script)
        # Replace strings with encoded versions
        for string in strings:
            if len(string) > 3:
                encoded = ''.join([f'chr({ord(c)})+' for c in string])[:-1]
                script = script.replace(f'"{string}"', f'({encoded})')
        return script
    
    def _obfuscate_python_control_flow(self, script):
        """Obfuscate control flow in Python script"""
        # Add random dead code
        dead_code = ''.join([f'if False: print("{''.join(random.choices(string.ascii_letters, k=20))}"); ' for _ in range(5)])
        script = dead_code + script
        # Add random comments
        lines = script.split('\n')
        for i in range(len(lines)):
            if lines[i].strip() and not lines[i].strip().startswith('#'):
                comment = ''.join(random.choices(string.ascii_letters, k=10))
                lines[i] = f'{lines[i]}  # {comment}'
        script = '\n'.join(lines)
        return script
    
    def pack_binary(self, binary_path):
        """Pack binary using current packer"""
        packer = self.evasion_techniques['binary']['current_packer']
        logger.info(f'Packing binary with {packer}')
        
        if packer == 'upx':
            # Check if upx is available
            if shutil.which('upx'):
                try:
                    subprocess.run(['upx', '--best', binary_path], check=True)
                    logger.info('Binary packed with UPX successfully')
                    return True
                except subprocess.CalledProcessError:
                    logger.error('Failed to pack binary with UPX')
                    return False
            else:
                logger.error('UPX is not available')
                return False
        
        elif packer == 'mpress':
            # Check if mpress is available
            if shutil.which('mpress'):
                try:
                    subprocess.run(['mpress', '/b', binary_path], check=True)
                    logger.info('Binary packed with MPRESS successfully')
                    return True
                except subprocess.CalledProcessError:
                    logger.error('Failed to pack binary with MPRESS')
                    return False
            else:
                logger.error('MPRESS is not available')
                return False
        
        elif packer == 'custom':
            # Use custom packing technique
            logger.info('Using custom packing technique')
            # For now, just return True as a placeholder
            return True
        
        return False
    
    def test_evasion(self, payload_path, av_scanner=None):
        """Test payload against antivirus scanners"""
        logger.info(f'Testing payload {payload_path} for evasion')
        
        # Calculate payload hash
        with open(payload_path, 'rb') as f:
            payload_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Simulate antivirus scan
        # In a real implementation, this would use an actual AV scanner or online service
        detection_result = self._simulate_av_scan(payload_path)
        
        # Record test result
        test_result = {
            'timestamp': datetime.datetime.now().isoformat(),
            'payload_path': payload_path,
            'payload_hash': payload_hash,
            'detection_result': detection_result,
            'evasion_techniques': self.evasion_techniques.copy()
        }
        
        self.test_results.append(test_result)
        logger.info(f'Evasion test completed: {detection_result}')
        return test_result
    
    def _simulate_av_scan(self, payload_path):
        """Simulate antivirus scan"""
        # Simulate detection based on payload type and obfuscation level
        payload_name = os.path.basename(payload_path)
        
        # Check if payload is a PowerShell script
        if payload_name.endswith('.ps1'):
            technique = self.evasion_techniques['powershell']['current_technique']
            if technique == 'basic':
                return {'detected': True, 'av_vendor': 'Windows Defender', 'signature': 'PowerShell obfuscation'}
            elif technique == 'medium':
                return {'detected': random.choice([True, False]), 'av_vendor': 'Avast', 'signature': 'Suspicious PowerShell script'}
            elif technique == 'advanced':
                return {'detected': False, 'av_vendor': None, 'signature': None}
        
        # Check if payload is a Python script
        elif payload_name.endswith('.py'):
            technique = self.evasion_techniques['python']['current_technique']
            if technique == 'basic':
                return {'detected': True, 'av_vendor': 'Kaspersky', 'signature': 'Python packed payload'}
            elif technique == 'medium':
                return {'detected': random.choice([True, False]), 'av_vendor': 'McAfee', 'signature': 'Suspicious Python script'}
            elif technique == 'advanced':
                return {'detected': False, 'av_vendor': None, 'signature': None}
        
        # Check if payload is a binary
        else:
            packer = self.evasion_techniques['binary']['current_packer']
            if packer == 'upx':
                return {'detected': random.choice([True, False]), 'av_vendor': 'Symantec', 'signature': 'Packed executable'}
            elif packer == 'mpress':
                return {'detected': random.choice([True, False]), 'av_vendor': 'Avast', 'signature': 'Packed executable'}
            elif packer == 'custom':
                return {'detected': False, 'av_vendor': None, 'signature': None}
        
        # Default result
        return {'detected': False, 'av_vendor': None, 'signature': None}
    
    def generate_evasion_report(self):
        """Generate evasion report"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'signature_database': self.signature_database,
            'evasion_techniques': self.evasion_techniques,
            'test_results': self.test_results
        }
        
        # Save report to file
        report_path = os.path.join(self.config.get_path('logs', dir=True), 'evasion_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f'Evasion report generated at {report_path}')
        return report
    
    def get_evasion_status(self):
        """Get current evasion status"""
        return {
            'signature_database': self.signature_database,
            'evasion_techniques': self.evasion_techniques,
            'last_update_check': self.last_update_check.isoformat() if self.last_update_check else None,
            'test_results_count': len(self.test_results)
        }